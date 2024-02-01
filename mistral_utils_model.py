import csv
import os
#from transformers import AutoTokenizer, AutoModelForCausalLM
#from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline, logging, set_seed
#from auto_gptq import AutoGPTQForCausalLM, BaseQuantizeConfig, exllama_set_max_input_length

def load_toy_dataset():
    # Specify the file name for the CSV
    csv_filename = "/data/Projects/Copilot/pipeline_generation/pipeline-decomposition/toy_dataset/toy_dataset.csv"

    # Initialize an empty list to store the loaded data
    loaded_dataset = []

    # Open the CSV file in read mode
    with open(csv_filename, mode="r") as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            loaded_dataset.append({
                "user_request": row["user_request"],
                "input_file_path": row["input_file_path"]
            })
            
    return loaded_dataset

def load_model(model_name, revision):
    model = AutoModelForCausalLM.from_pretrained(model_name,
                                                 device_map = {"model": 3, "lm_head": 3, },
                                                 trust_remote_code=False,
                                                 revision=revision,
                                                 )
    model.tie_weights()
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
    return model, tokenizer

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
Job 1: {{"id": 1, "dep": 0, "name": job_name, "description": job_description, "input_resources": ""example1.ext", "example2.ext"", "output_resources": ""example1.ext", "example2.ext""}}
Job 2: {{"id": 2, "dep": dependency_job_ids, "name": job_name, "description": job_description, "input_resources": ""example1.ext", "example2.ext"", "output_resources": ""example1.ext", "example2.ext""}}
Job 3: {{"id": 3, "dep": dependency_job_ids, "name": job_name, "description": job_description, "input_resources": ""example1.ext", "example2.ext"", "output_resources": ""example1.ext", "example2.ext""}}
...
Job N: {{"id": N, "dep": dependency_job_ids, "name": job_name, "description": job_description, "input_resources": ""example1.ext", "example2.ext"", "output_resources": ""example1.ext", "example2.ext""}}
[/PIPELINE]

The "dep" field denotes the id of the previous Job which generates a new resource upon which the current Job relies, 0 otherwise.
The "description" field describes the objective of the Job. Also, it includes all the necessary guidelines for generating the Python script that corresponds to this Job.
The "input_resources" field corresponds to the resources that a Job needs to access to be executed. It can be files and or databases... Most of the time, these resources correspond to 'output_resources' from other Jobs. You should give a probable name and the appropriate extension to these files. 
The "output_resources" field corresponds to the resources that were modified/created by the current Job. It can be paths to access files or databases..

You are also able to modify one of your previous propositions if the user is asking you to (add/delete/modify : jobs, descriptions, resources...). 
Here is the history of the conversation to better understand the context of the user's request. Remember that your objective is to helpfully and precisely fulfill the last request of the user :
{format_previous_messages_as_string(previous_messages)}

Here is the user request that you must fulfill:
User : {user_request}

[/INST]
''' 
    return prompt


def extract_pipeline_decomposition(data):
    # Remove the instruction prompt
    if '[/INST]' in data:
        data = data[data.find('[/INST]'):]

    # Extract the task decompostion
    try:
        #data = data[data.find('[TASKS]'):data.find('[/TASKS]')]
        data = data[data.find('[PIPELINE]'):data.find('[/PIPELINE]')]
    except NameError:
        print('Can not extract the list of tasks from the output of the LLM')

    start_pattern = '{"id'
    end_pattern = '}\n'
    # Get the indexes of the start/end of the task in the data
    start_idx = [i for i in range(len(data)) if data.startswith(start_pattern, i)]
    end_idx = [i+len(end_pattern) for i in range(len(data)) if data.startswith(end_pattern, i)]

    if (len(start_idx) != len(end_idx)):
        print(f'Found {len(start_idx)} start indexes VS {len(end_idx)} end indexes.\n')    
        print(f'{start_idx=}')
        print(f'{end_idx=}')
        tasks = None
        print(data)
    else:
        # Use eval() to convert parsed string into python dict() variable
        tasks = [eval(data[start_idx[i]:end_idx[i]].replace("\n","")) for i in range(len(start_idx))]
    print(f'{tasks=}')
    for task in tasks:
        if task['dep'] == []:
            task['dep'] = [0]
    return tasks

def generate_one_code_generation_prompt(task):
    # Build the prompt
    prompt =f'''[INST] You are an expert software engineer, your goal is to write a Python script that solves the task of "{task['name']}". 
The script should use these resources as input : {task['input_resources']}, perform the following task on it :  "{task['name']} : {task['description']}". The execution of your script on the input resources should generate these resources : {task['output_resources']}. 
Don't forget to import the necessary libraries at the beggining of the script.
Your generated code must follow the following format, starting with a [PYTHON] tag and ending with a [/PYTHON] tag.
[/INST]

[PYTHON]
'''
    print(f'''*** Generating code for Task ID n° {task['id']} : {task['name']} ***''')
    #input_ids = tokenizer(prompt, return_tensors='pt').input_ids.cuda('cuda:3')
    #output = model.generate(inputs=input_ids, temperature=0.5, do_sample=True, top_p=0.95, top_k=40, max_new_tokens=1024)
    #output = tokenizer.decode(output[0])
    
    return prompt

def generate_codes_for_all_tasks(model, tokenizer, tasks):
    outputs_lm2 = []
    for task in tasks:
        output = generate_output_for_one_task(model, tokenizer, task)
        outputs_lm2.append(output)    
        
    return outputs_lm2

def generate_whole_code_generation_prompt(previous_messages, user_request):
    # Remove the old messages ( we only keep the last 2 messages)
    if len(previous_messages) > 2:
        previous_messages = previous_messages[-2:]
        
    prompt = f'''[INST] <<SYS>>You are a helpful AI assistant that helps users to generate Python scripts. Given a Pipeline and a user request, your objective is to generate the Python code of one or multiple Job(s) of the given Pipeline to match the user's request.
A Pipeline is a list of multiple tasks (also called "Jobs") with dependencies.
Your generated Pipeline must follow the following format, starting with a [PIPELINE] tag and end with a [/PIPELINE] tag:
[PIPELINE]
Job 1: {{"id": 1, "dep": 0, "name": job_name, "description": job_description, "input_resources": ""example1.ext", "example2.ext"", "output_resources": ""example1.ext", "example2.ext"", "code": python_code}}
Job 2: {{"id": 2, "dep": dependency_job_ids, "name": job_name, "description": job_description, "input_resources": ""example1.ext", "example2.ext"", "output_resources": ""example1.ext", "example2.ext"", "code": python_code}}
Job 3: {{"id": 3, "dep": dependency_job_ids, "name": job_name, "description": job_description, "input_resources": ""example1.ext", "example2.ext"", "output_resources": ""example1.ext", "example2.ext"", "code": python_code}}
...
Job N: {{"id": N, "dep": dependency_job_ids, "name": job_name, "description": job_description, "input_resources": ""example1.ext", "example2.ext"", "output_resources": ""example1.ext", "example2.ext"", "code": python_code}}
[/PIPELINE]

The "dep" field denotes the id of the previous Job which generates a new resource upon which the current Job relies, 0 otherwise.
The "description" field describes the objective of the Job. Also, it includes all the necessary guidelines for generating the Python script that corresponds to this Job.
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
    Given the whole answer of Mistral, extracts the Python code.
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
    # Create a new folder for the pipeline job files
    pipeline_number = 0
    while os.path.exists(f'''/data/Projects/Copilot/pipeline_generation/chat_model_app/jobs_python_files/pipeline_{pipeline_number}''') and pipeline_number < 50:
        pipeline_number += 1 

    directory_path = f'''/data/Projects/Copilot/pipeline_generation/chat_model_app/jobs_python_files/pipeline_{pipeline_number}'''
    os.mkdir(directory_path)

    for task in pipeline_decomposition_with_code:
        # Get the filename from the generated command line
        filename = f'''job_{task['id']}.py'''
        #filename = task['cmd_line'].split(' ')[1]
        
        # Store the Python file path
        task['python_file_path'] = f'''{directory_path}/{filename}'''
        
        # Open Python job file
        python_file = open(f'''{directory_path}/{filename}''', "w")

        # Write string to file
        python_file.write(task['code'])

        # Close file
        python_file.close()
        
def clear_folder():
    folder_path = '/data/Projects/Copilot/pipeline_generation/pipeline-decomposition/jobs_python_files/'
    for root, dirs, files in os.walk(folder_path, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))