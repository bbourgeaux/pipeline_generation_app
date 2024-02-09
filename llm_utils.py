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

def generate_one_pipeline_decomposition_prompt(previous_messages, user_request):
    # Remove the old messages ( we only keep the last 2 messages)
    if len(previous_messages) > 2:
        previous_messages = previous_messages[-2:]
        
    prompt = f'''[INST] <<SYS>>You are a helpful AI assistant that helps users to generate "Pipelines" or "Jobs".
Given a user request, determine if the user is asking you to generate a "Pipeline" or a "Job". A Pipeline is a list of multiple tasks (also called "Jobs") with dependencies. 
If not mentioned by the user, generate a Pipeline (generally between 3 and 8 Jobs). 
If the user explicitly asks for a Job, generate a Pipeline containing one single Job.
Each Job should be described with precision and in a logical order. Each Job must be performable by a Python script, and therefore should be easily translated into code.

Your generated Pipeline must follow the following format, starting with a [PIPELINE] tag and end with a [/PIPELINE] tag:
[PIPELINE]
Pipeline: {{"name": pipeline_name, "description": pipeline_description}}
Job 1: {{"id": 1, "dep": 0, "name": job_name, "description": job_description, "input_resources": ""example1.ext", "example2.ext"", "output_resources": ""example1.ext", "example2.ext""}}
Job 2: {{"id": 2, "dep": dependency_job_id, "name": job_name, "description": job_description, "input_resources": ""example1.ext", "example2.ext"", "output_resources": ""example1.ext", "example2.ext""}}
Job 3: {{"id": 3, "dep": dependency_job_id, "name": job_name, "description": job_description, "input_resources": ""example1.ext", "example2.ext"", "output_resources": ""example1.ext", "example2.ext""}}
...
Job N: {{"id": N, "dep": dependency_job_id, "name": job_name, "description": job_description, "input_resources": ""example1.ext", "example2.ext"", "output_resources": ""example1.ext", "example2.ext""}}
[/PIPELINE]

The "dep" field denotes the id of the previous Job which generates a new resource upon which the current Job relies, 0 otherwise.
The "description" field describes the objective of the Job (or Pipeline). Also, it includes all the necessary guidelines for generating the Python script that corresponds to this Job.
The "input_resources" field corresponds to the resources that a Job needs to access to be executed. Most of the time, these resources correspond to 'output_resources' from other Jobs. You should give a probable name and the appropriate extension to these files.
The "output_resources" field corresponds to the resources that were modified/created by the current Job. You should give a probable name and the appropriate extension to these files.

You are also able to modify one of your previous propositions if the user is asking you to (add/delete/modify : jobs, descriptions, resources...). 
Here is the history of the conversation to better understand the context of the user's request. Remember that your objective is to helpfully and precisely fulfill the last request of the user :
{format_previous_messages_as_string(previous_messages)}

Here is the user request that you must fulfill:
User : {user_request}

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
        data = data[data.find('[/INST]'):]

    # Extract the Pipeline
    try:
        pipeline_string = data[data.find('[PIPELINE]'):data.find('[/PIPELINE]')]
    except NameError:
        print('Can not extract the Pipeline from the output of the LLM')

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
                'name': pipeline_data['name'],
                'description': pipeline_data['description'],
                'jobs': []
            })
        else:
            job_data = json.loads(section_content)
            pipeline['jobs'].append({
                'id': job_data['id'],
                'dep': job_data['dep'],
                'name': job_data['name'],
                'description': job_data['description'],
                'input_resources': job_data['input_resources'],
                'output_resources': job_data['output_resources']
            })

    # Output the pipeline dictionary
    return pipeline

def generate_one_code_generation_prompt(job):
    # Build the prompt
    prompt =f'''[INST] You are an expert software engineer, your goal is to write a Python script that solves the job of "{job['name']}". 
The script should use these resources as input : {job['input_resources']}, perform the following job on it :  "{job['name']} : {job['description']}". The execution of your script on the input resources should generate these resources : {job['output_resources']}. 
Don't forget to import the necessary libraries at the beggining of the script.
Your generated code must follow the following format, starting with a [PYTHON] tag and ending with a [/PYTHON] tag.
[/INST]

[PYTHON]
'''
    print(f'''*** Generating code for job ID n° {job['id']} : {job['name']} ***''')
    return prompt

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
Job 2: {{"id": 2, "dep": dependency_job_id, "name": job_name, "description": job_description, "input_resources": ""example1.ext", "example2.ext"", "output_resources": ""example1.ext", "example2.ext"", "code": python_code}}
Job 3: {{"id": 3, "dep": dependency_job_id, "name": job_name, "description": job_description, "input_resources": ""example1.ext", "example2.ext"", "output_resources": ""example1.ext", "example2.ext"", "code": python_code}}
...
Job N: {{"id": N, "dep": dependency_job_id, "name": job_name, "description": job_description, "input_resources": ""example1.ext", "example2.ext"", "output_resources": ""example1.ext", "example2.ext"", "code": python_code}}
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

def extract_code_from_output(raw_output):
    """
    Given the whole answer of the LLM, extracts the Python code.
    """
    raw_output
    
    # Remove the instruction prompt
    if '[/INST]' in raw_output:
        raw_output = raw_output[raw_output.find('[/INST]'):]
    '''
    # Extract the command line
    start_pattern = '[/CMD]' # should be '[CMD]' 
    end_pattern = '</s>' # should be '[/CMD]'
    if start_pattern not in raw_output:
        raise ValueError(f'Substring "{start_pattern}" not found in the output of the LLM.')
    elif end_pattern not in raw_output:
        raise ValueError(f'Substring "{end_pattern}" not found in the output of the LLM.')
    else:
        start_idx = raw_output.find(start_pattern) + len(start_pattern)
        end_idx = raw_output.find(end_pattern)
        cmd_line = raw_output[start_idx:end_idx] 
        
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
    
    return python_code

def create_python_files(pipeline_decomposition_with_code):
    print(f'{os.getcwd()}')
    flask_app_dir = os.getcwd()
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