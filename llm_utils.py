import os
import re
import json

def format_previous_messages_as_string(messages):
    if len(messages) < 1:
        return ''
    user_content = messages[0]['content']
    assistant_content = ""
    
    for job in messages[1]['content']:
        assistant_content += f"Job {job['id']} - {job['name']}\n"
        assistant_content += f"Description: {job['description']}\n"
        assistant_content += f"Input Resources: {', '.join(job['input_resources'])}\n"
        assistant_content += f"Output Resources: {', '.join(job['output_resources'])}\n\n"

    result_string = f"User: {user_content}\nAssistant: {assistant_content}"
    return result_string

def format_previous_messages_as_string(messages):
    result_string = ""
    if len(messages) > 1:
        for message in messages:
        
            if message['role'] == 'user': # Format User's messages
                user_content = message['content']
                result_string += f"\nUser: {user_content}"

            elif message['role'] == 'assistant': # Format Assistant's messages
                assistant_content = ""
                for job in message['content']:
                    assistant_content += f"Job {job['id']} - {job['name']}\n"
                    assistant_content += f"Description: {job['description']}\n"
                    assistant_content += f"Input Resources: {', '.join(job['input_resources'])}\n"
                    assistant_content += f"Output Resources: {', '.join(job['output_resources'])}\n"
                result_string += f"\nAssistant: {assistant_content}"

    return result_string

def format_previous_messages_as_string(messages):
    result_string = ""
    if len(messages) > 1:
        for message in messages:
        
            if message['role'] == 'user': # Format User's messages
                user_content = message['content']
                result_string += f"\nUser: {user_content}"
                
            elif message['role'] == 'assistant': # Format Assistant's messages
                assistant_content = message['content']
                result_string += f"\nAssistant: {assistant_content}"

    return result_string

def generate_one_pipeline_decomposition_prompt(previous_messages, user_message):

    prompt = f'''[INST] <<SYS>>You are a helpful AI assistant that helps users to generate "Pipelines" or "Jobs".
Given a user request, determine if the user is asking you to generate a "Pipeline" or a "Job". A Pipeline is a list of multiple tasks (also called "Jobs") with dependencies. 
If not mentioned by the user, generate a Pipeline (generally between 3 and 8 Jobs). 
If the user explicitly asks for a Job, generate a Pipeline containing one single Job.
Each Job should be described with precision and in a logical order. Each Job must be performable by a Python script, and therefore should be easily translated into code.

Your generated Pipeline must follow the following format, starting with a [PIPELINE] tag and end with a [/PIPELINE] tag:
[PIPELINE]
Pipeline: {{"name": pipeline_name, "description": pipeline_description}}
Job 1: {{"id": 1, "dep": 0, "name": job_name, "description": job_description, "input_resources": "example.ext", "output_resources": "example.ext"}}
Job 2: {{"id": 2, "dep": 1, "name": job_name, "description": job_description, "input_resources": "example.ext", "output_resources": "example.ext"}}
Job 3: {{"id": 3, "dep": 2, "name": job_name, "description": job_description, "input_resources": "example.ext", "output_resources": "example.ext"}}
...
Job N: {{"id": N, "dep": N-1, "name": job_name, "description": job_description, "input_resources": "example.ext", "output_resources": "example.ext"}}
[/PIPELINE]

The "dep" field denotes the id of the previous Job which generates a new resource upon which the current Job relies, 0 otherwise.
The "description" field describes the objective of the Job (or Pipeline). Also, it includes all the necessary guidelines for generating the Python script that corresponds to this Job.
The "input_resources" field corresponds to the resources that a Job needs to access to be executed. Most of the time, these resources correspond to 'output_resources' from other Jobs. You should give a probable name and the appropriate extension to these files.
The "output_resources" field corresponds to the resources that were modified/created by the current Job. You should give a probable name and the appropriate extension to these files.

You are also able to modify one of your previous propositions if the user is asking you to (add/delete/modify : jobs, descriptions, resources...). If the user is not asking for the creation of a Pipeline, kindly answer his question and remind him that your objective is to help him create the Pipeline he wants in Saagie.
Here is the history of the conversation to better understand the context of the user's request. Remember that your objective is to helpfully and precisely fulfill the last request of the user :
{format_previous_messages_as_string(previous_messages)}

Here is the user request that you must fulfill:
User : {user_message}

[/INST]
''' 
    return prompt

def generate_one_pipeline_decomposition_from_image_prompt(extracted_texts):
        
    prompt = f'''[INST] <<SYS>>You are a helpful AI assistant that helps users to generate "Pipelines" or "Jobs".
 A Pipeline is a list of multiple tasks (also called "Jobs") with dependencies.

Your reconstructed Pipeline must follow the following format, starting with a [PIPELINE] tag and end with a [/PIPELINE] tag:
[PIPELINE]
Pipeline: {{"name": pipeline_name, "description": pipeline_description}}
Job 1: {{"id": 1, "dep": 0, "name": job_name, "description": job_description, "input_resources": "example.ext", "output_resources": "example.ext"}}
Job 2: {{"id": 2, "dep": 1, "name": job_name, "description": job_description, "input_resources": "example.ext", "output_resources": "example.ext"}}
Job 3: {{"id": 3, "dep": 2, "name": job_name, "description": job_description, "input_resources": "example.ext", "output_resources": "example.ext"}}
...
Job N: {{"id": N, "dep": N-1, "name": job_name, "description": job_description, "input_resources": "example.ext", "output_resources": "example.ext"}}
[/PIPELINE]

The "dep" field denotes the id of the previous Job which generates a new resource upon which the current Job relies, 0 otherwise.
The "description" field describes the objective of the Job (or Pipeline). Also, it includes all the necessary guidelines for generating the Python script that corresponds to this Job.
The "input_resources" field corresponds to the resources that a Job needs to access to be executed. Most of the time, these resources correspond to 'output_resources' from other Jobs. You should give a probable name and the appropriate extension to these files.
The "output_resources" field corresponds to the resources that were modified/created by the current Job. You should give a probable name and the appropriate extension to these files.

You will be given a list of elements that belong to the Pipeline (Job names, descriptions, resources). 
Your objective is to associate them to fielsd of the Jobs in a meaningful way to reconstruct the Pipeline.
You should first determine if the information are only the names of the Jobs, or the Jobs and descriptions, or if there is also the input/output resources.
If some fields are missing, you are not allowed to create them, but you can leave them blank.
You are not allowed to fill multiple fields with the same information.
If the information provided only contains Job names, your reconstructed Pipeline should only contain Job names and leave other fields blank.

Remember that you can only use the elements given below, you can't guess, add, invent ANYTHING.

Here are the only elements that are given to you : 
{extracted_texts}

[/INST]
''' 
    return prompt

'''
def extract_pipeline_decomposition(data):
    # Remove the instruction prompt
    if '[/INST]' in data:
        data = data[data.find('[/INST]'):]

    # Extract the Pipeline
    try:
        data = data[data.find('[PIPELINE]'):data.find('[/PIPELINE]')]
    except NameError:
        print('Can not extract the Pipeline from the output of the LLM')

    start_pattern = '{"id'
    end_pattern = '}\n'
    # Get the indexes of the start/end of the job in the data
    start_idx = [i for i in range(len(data)) if data.startswith(start_pattern, i)]
    end_idx = [i+len(end_pattern) for i in range(len(data)) if data.startswith(end_pattern, i)]

    if (len(start_idx) != len(end_idx)):
        print(f'Found {len(start_idx)} start indexes VS {len(end_idx)} end indexes.\n')    
        print(f'{start_idx=}')
        print(f'{end_idx=}')
        jobs = None
        print(data)
    else:
        # Use eval() to convert parsed string into python dict() variable
        jobs = [eval(data[start_idx[i]:end_idx[i]].replace("\n","")) for i in range(len(start_idx))]
    print(f'{jobs=}')
    for job in jobs:
        if job['dep'] == []:
            job['dep'] = [0]
    return jobs
'''

def extract_pipeline_decomposition(data):
    # Remove the instruction prompt
    if '[/INST]' in data:
        data = data[data.find('[/INST]')+len('[/INST]'):]

    # Extract the Pipeline
    starting_tag = '[PIPELINE]'
    ending_tag = '[/PIPELINE]'
    if starting_tag in data and ending_tag in data:
        pipeline_string = data[data.find(starting_tag)+len(starting_tag):data.find(ending_tag)]
    else:
        while data.startswith('\n'):
            data = data[1:]

        return None, data

    # Pattern for extracting each section
    pattern = r'(\w+\s?\d*): (.*?)(?=\n\w|\n\[|\n$)'

    # Extracting sections
    sections = re.findall(pattern, pipeline_string, re.DOTALL)

    # Initialize pipeline dictionary
    pipeline = {}

    # Iterate over sections and add to pipeline dictionary
    for section_name, section_content in sections:
        if section_name == "Pipeline":
            pipeline_data = json.loads(section_content)
            pipeline.update({
                "name": pipeline_data["name"],
                "description": pipeline_data["description"],
                "jobs": []
            })
        else:
            job_data = json.loads(section_content)
            # If those fields were not generated, leave them empty
            if "input_resources" not in job_data:
                job_data["input_resources"] = ""
            if "output_resources" not in job_data:
                job_data["output_resources"] = ""

            pipeline["jobs"].append({
                #"id": job_data["id"],
                #"dep": job_data["dep"],
                "name": job_data["name"],
                "description": job_data["description"],
                "input_resources": job_data["input_resources"],
                "output_resources": job_data["output_resources"]
            })
    print(pipeline)
    for i in range(len(pipeline["jobs"])):
        pipeline["jobs"][i]["id"] = str(i+1)
        pipeline["jobs"][i]["dep"] = str(i)

    # Output the pipeline dictionary
    return pipeline, pipeline_string

def generate_one_code_generation_prompt_old(job, previous_messages, user_message):
    # Build the prompt
    prompt =f'''[INST] You are an expert software engineer, your goal is to write a Python script that solves the job of "{job["name"]}". 
The script should use these resources as input : {job["input_resources"]}, perform the following job on it :  "{job["name"]} : {job["description"]}". The execution of your script on the input resources should generate these resources : {job["output_resources"]}. 
Don't forget to import the necessary libraries at the beggining of the script.
Your generated code must follow the following format, starting with a [PYTHON] tag and ending with a [/PYTHON] tag.
[/INST]

[PYTHON]
'''
    print(f'''*** Generating code for job ID n° {job["id"]} : {job["name"]} ***''')
    return prompt

def generate_first_code_generation_prompt(job, previous_messages, user_message):
    # Build the prompt
    prompt =f'''[INST] You are an expert software engineer, your goal is to write a Python script that solves the job of "{job["name"]}". 
The script should use these resources as input : {job["input_resources"]}, perform the following job on it :  "{job["name"]} : {job["description"]}". The execution of your script on the input resources should generate these resources : {job["output_resources"]}. 
Don't forget to import the necessary libraries at the beggining of the script.
You are not allowed to leave some steps "TODO" in your code, you must write the code to perform these steps.
Your generated code must follow the following format, starting with a [PYTHON] tag and ending with a [/PYTHON] tag.

Here is the history of the conversation to better understand the context of the user's request. Remember that your objective is to helpfully and precisely fulfill the last request of the user :
{format_previous_messages_as_string(previous_messages)}

Here is the user request that you must fulfill:
User : {user_message}
[/INST]

[PYTHON]
'''
    print(f'''*** Generating code for job ID n° {job["id"]} : {job["name"]} ***''')
    return prompt

def generate_iteration_on_code_generation_prompt(job, user_message):
    # Build the prompt
    prompt =f'''[INST] You are an expert software engineer, your goal is to modify Python scripts to incorporate modifications specified by your client.
The modification you will make to the script will not change the input/output resources of the script.

Here are the initial specifications of the script :
The script should solve this task : "{job["name"]}" : {job["description"]}". 
The script should use these resources as input : {job["input_resources"]}, perform the following job on it :  "{job["name"]} : {job["description"]}".
The execution of the script on the input resources should generate these resources : {job["output_resources"]}. 
Import the necessary libraries at the beggining of the script.

Here is the current version of the code to better understand the context of the client's request. Remember that your objective is to helpfully and precisely modify the Python script to satisfy the client :
{job['code']}

Here is the modification that the client is requesting :
User : {user_message}

Your generated code must follow the following format, starting with a [PYTHON] tag and ending with a [/PYTHON] tag.
[/INST]

[PYTHON]
'''
    print(f'''*** Iterating on code for job ID n° {job["id"]} : {job["name"]} ***''')
    return prompt

def generate_determine_iteration_requests_prompt(pipeline_decomposition, user_message):
    formatted_jobs = ""
    for job in pipeline_decomposition['jobs']:
        formatted_jobs += f"Job {job['id']}: {job['name']}\n"

    # Remove the trailing newline character
    formatted_jobs = formatted_jobs.rstrip("\n")
    # Build the prompt
    prompt =f'''[INST] You are an expert software engineer, and your goal is to help the user modify some Python code. 
You have already given code, now the user is asking you to modify the code of the Jobs. 
The user request is global : it can concern one Job, multiple Jobs, or all Jobs.
Your objective is to determine which Jobs need to be modified to fulfill the user request. Also, if a Job is concerned by the user request, you must adapt the request to be specific to that Job.
If the user did not mention any Jobs explicitly, you must consider ALL Jobs.

Your generated list must follow the following format including ALL jobs, starting with a [REQUESTS] tag and end with a [/REQUESTS] tag:
[REQUESTS]
Job 1: {{"is_concerned_by_user_request": Boolean, "adapted_request": String}}
Job 2: {{"is_concerned_by_user_request": Boolean, "adapted_request": String}}
...
Job N: {{"is_concerned_by_user_request": Boolean, "adapted_request": String}}
[/REQUESTS]

The "is_concerned_by_user_request" field is a Boolean, it denotes whether the Job is concerned by the user request and should me modified or not.
The "adapted_request" field corresponds to the adapted user request that is specific to the Job. If the Job is not concerned by the user request, the "adapted_request" field is an empty string.

Here is the structure of the pipeline and its different Jobs : 
{formatted_jobs}

Remember that your list should also have {len(pipeline_decomposition['jobs'])} jobs. It must include all Jobs, including the one that don't need to be modified.

Here is the initial user request :
{user_message}

[/INST]
'''
    return prompt

def extract_iteration_requests(data):
    # Remove the instruction prompt
    if '[/INST]' in data:
        data = data[data.find('[/INST]')+len('[/INST]'):]

    # Extract the Requests
    starting_tag = '[REQUESTS]'
    ending_tag = '[/REQUESTS]'
    if starting_tag in data and ending_tag in data:
        requests_string = data[data.find(starting_tag)+len(starting_tag):data.find(ending_tag)]
    else:
        while data.startswith('\n'):
            data = data[1:]
        return None, data

    # Split requests_string into individual sections
    sections = requests_string.strip().split('\n')

    # Initialize list to store parsed requests
    requests = []

    # Iterate over sections and parse JSON data
    for section in sections:
        # Extract job number and JSON data
        job_number, json_data = section.split(': ', 1)
        job_number = job_number.split(' ')[-1]
        json_data = json_data.replace('True', 'true')
        json_data = json_data.replace('False', 'false')
        job_data = json.loads(json_data)
        
        # Add parsed data to requests list
        requests.append({
            "job_number": job_number.strip(),
            "is_concerned_by_user_request": job_data["is_concerned_by_user_request"],
            "adapted_request": job_data["adapted_request"]
        })

    # Output the list of parsed requests
    return requests, requests_string

def generate_whole_code_generation_prompt(previous_messages, user_request):
    # Remove the old messages ( we only keep the last 2 messages)
    if len(previous_messages) > 2:
        previous_messages = previous_messages[-2:]
        
    prompt = f'''[INST] <<SYS>>You are a helpful AI assistant that helps users to generate Python scripts. Given a Pipeline and a user request, your objective is to generate the Python code of one or multiple Job(s) of the given Pipeline to match the user's request.
A Pipeline is a list of multiple tasks (also called "Jobs") with dependencies.
Your generated Pipeline must follow the following format, starting with a [PIPELINE] tag and end with a [/PIPELINE] tag:
[PIPELINE]
Pipeline: {{"name": pipeline_name, "description": pipeline_description}}
Job 1: {{"id": 1, "dep": 0, "name": job_name, "description": job_description, "input_resources": ""example1.ext", "example2.ext"", "output_resources": ""example1.ext", "example2.ext"", "code": python_code}}
Job 2: {{"id": 2, "dep": 1, "name": job_name, "description": job_description, "input_resources": ""example1.ext", "example2.ext"", "output_resources": ""example1.ext", "example2.ext"", "code": python_code}}
Job 3: {{"id": 3, "dep": 2, "name": job_name, "description": job_description, "input_resources": ""example1.ext", "example2.ext"", "output_resources": ""example1.ext", "example2.ext"", "code": python_code}}
...
Job N: {{"id": N, "dep": N-1, "name": job_name, "description": job_description, "input_resources": ""example1.ext", "example2.ext"", "output_resources": ""example1.ext", "example2.ext"", "code": python_code}}
[/PIPELINE]

The "dep" field denotes the id of the previous Job which generates a new resource upon which the current Job relies, 0 otherwise.
The "description" field describes the objective of the Job (or Pipeline). Also, it includes all the necessary guidelines for generating the Python script that corresponds to this Job.
The "input_resources" field corresponds to the resources that a Job needs to access to be executed. It can be files and or databases... Most of the time, these resources correspond to 'output_resources' from other Jobs. You should give a probable name and the appropriate extension to these files. 
The "output_resources" field corresponds to the resources that were modified/created by the current Job. It can be paths to access files or databases..
The "code" field corresponds to the Python code that corresponds to the Job's description. It is the most important field, you need to generate Python code for it. 

You are also able to modify one of your previous propositions if the user is asking you to (add/delete/modify the code of one or multiple Jobs...). In this case, you are only allowed to modify the "code" field(s) of the Job(s) the user is asking you. 
You must generate the whole Pipeline including the parts you didn't change and your modifications/generations.
Here is the history of the conversation to better understand the context of the user's request. Remember that your objective is to helpfully and precisely fulfill the last request of the user :
{format_previous_messages_as_string(previous_messages)}

Here is the user request that you must fulfill:
User : {user_request}

[/INST]
''' 
    return prompt

def extract_code_from_output(llm_output):
    """
    Given the whole answer of the LLM, extracts the Python code.
    """

    # Remove the instruction prompt
    if '[/INST]' in llm_output:
        llm_output = llm_output[llm_output.find('[/INST]'):]


    # Extract the Pipeline
    try:
        starting_tag = '[PYTHON]'
        ending_tag = '[/PYTHON]'
        # If the output reached the maximum number of tokens without generating the ending_tag, we manually add it to the end of the llm_output.
        if ending_tag not in llm_output:
            llm_output += ending_tag
        code_string = llm_output[llm_output.find(starting_tag)+len(starting_tag):llm_output.find(ending_tag)]
    except NameError:
        print('Can not extract the Pipeline from the output of the LLM')

    # Remove leading newline characters
    while code_string.startswith('\n'):
        code_string = code_string[1:]

    # Remove trailing newline characters
    while code_string.endswith('\n'):
        code_string = code_string[:-1]

    '''    
    # Extract the Python code
    start_pattern = '[PYTHON]\n'
    end_pattern = '[/PYTHON]'
    if start_pattern not in raw_output:
        raw_output = start_pattern + raw_output
        #print(raw_output)
        #raise ValueError(f'Substring "{start_pattern}" not found in the output of the LLM.')
    if end_pattern not in raw_output:
        raw_output += end_pattern
        print(raw_output)
        #raise ValueError(f'Substring "{end_pattern}" not found in the output of the LLM.')
        #print(f'Substring "{end_pattern}" not found in the output of the LLM.')
        #end_pattern = '</s>'
    start_idx = raw_output.find(start_pattern) + len(start_pattern)
    end_idx = raw_output.find(end_pattern)
    python_code = raw_output[start_idx:end_idx] 
        
    # If the command line is in the Python code, remove it
    if '[/CMD]' in python_code:
        python_code = python_code[:python_code.find('[/CMD]')]
    '''
    return code_string

def create_python_files(pipeline_decomposition_with_code, flask_app_dir):
    # Create a new folder for the pipeline job files
    pipeline_number = 0
    while os.path.exists(f'''{flask_app_dir}/tmp/pipeline_{pipeline_number}''') and pipeline_number < 50:
        pipeline_number += 1 

    directory_path = f'''{flask_app_dir}/tmp/pipeline_{pipeline_number}'''
    os.mkdir(directory_path)

    for job in pipeline_decomposition_with_code['jobs']:
        # Get the filename from the generated command line
        filename = f'''job_{job['id']}.py'''
        
        # Store the Python file path
        job['python_file_path'] = f'''{directory_path}/{filename}'''
        
        # Open Python job file
        python_file = open(f'''{directory_path}/{filename}''', "w")

        # Write string to file
        python_file.write(job['code'])

        # Close file
        python_file.close()
        
def clear_folder():
    folder_path = './tmp/'
    for root, dirs, files in os.walk(folder_path, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))

def build_pipeline_decomposition_from_ocr(texts):
        
    #job_names = texts.split('\n')
    
    # Create an empty pipeline decomposition
    pipeline_decomposition = {
        "name": "Pipeline extracted by OCR",
        "description": "Pipeline extracted  from input image using OCR",
        "jobs": []
    }
    # Manually add jobs to the pipeline decomposition
    for i in range(len(job_names)):
        job = {}
        job["id"] = str(i+1)
        job["name"] = job_names[i]
        job["dep"] = str(i)
        job["description"] = ""
        job["input_resources"] = []
        job["output_resources"] = []

        pipeline_decomposition["jobs"].append(job)

    return pipeline_decomposition