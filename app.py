from flask import Flask, render_template, request, jsonify
import requests
import os
import urllib3
import logging
from llm_utils import (
    generate_one_pipeline_decomposition_prompt,
    generate_one_pipeline_decomposition_from_image_prompt,
    extract_pipeline_decomposition,
    generate_first_code_generation_prompt,
    generate_iteration_on_code_generation_prompt,
    generate_determine_iteration_requests_prompt,
    extract_iteration_requests,
    extract_code_from_output,
    create_python_files
)
from saagieapi_utils import create_pipeline_in_saagie

app = Flask(__name__)

ENV_VARS = ['LLM_SERVER_URL', 'SAAGIE_PLATFORM_URL', 'SAAGIE_PROJECT_ID', 'SAAGIE_USER_NAME', 'SAAGIE_USER_PASSWORD']
APP_DIR = os.getcwd()
GENERIC_ERROR_MESSAGE = "I can be really helpful in creating jobs and pipelines but beyond this scope, you should talk to someone more knowledgeable."


# Remove a particular warning regarding Certificate Verification (HTTPS requests)
urllib3.disable_warnings(urllib3.exceptions.SubjectAltNameWarning)

previous_messages = []
pipeline_decompositions = []
env_var_are_set = False

@app.route('/', methods=['GET', 'POST'])
def chat():
    return render_template("index.html")

@app.route('/restart', methods=['POST'])
def restart():
    global previous_messages
    global pipeline_decompositions
    global env_var_are_set

    previous_messages = []
    pipeline_decompositions = []
    env_var_are_set = False

    return jsonify({"message": "App restarted successfully"})

@app.route('/generate-response', methods=['POST'])
def generate_response():
    global env_var_are_set
    try:
        if not env_var_are_set:
            env_var_are_set = check_if_env_variables_are_set(ENV_VARS)
        app.logger.info("1")
        task = request.json.get('task', '')        
        app.logger.info("2")
        app.logger.info(task)

        user_message = request.json.get('user_message', '')
        app.logger.info("3")

        if task == 'pipeline_decomposition':
            app.logger.info("4")
            pipeline_decomposition_response = handle_pipeline_decomposition(user_message)
            return jsonify(pipeline_decomposition_response)

        elif task == 'first_code_generation':
            code_generation_response = handle_first_code_generation(user_message)
            return jsonify(code_generation_response)
        
        elif task == 'iteration_on_code_generation':
            code_generation_response = handle_iteration_on_code_generation(user_message)
            return jsonify(code_generation_response)

        elif task == 'creation_in_saagie':
            saagie_creation_response = handle_saagie_creation()
            return jsonify(saagie_creation_response)

        else:
            return jsonify({"error": "Invalid task specified"}), 400

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500
    
@app.route('/pipeline-decomposition-from-image', methods=['POST'])
def pipeline_decomposition_from_imagee():
    global env_var_are_set
    try:
        if not env_var_are_set:
            env_var_are_set = check_if_env_variables_are_set(ENV_VARS)
        app.logger.info(f"{request.files=}")
        task = request.form.get('task', '')  # Access form data using request.form

        if task == 'pipeline_decomposition':
            file = request.files['file']
            #file.save(os.path.join('./tmp', file.filename))
            pipeline_decomposition_response = handle_pipeline_decomposition_from_image(file)
            return jsonify(pipeline_decomposition_response)
        else: 
            return jsonify({"error": "Invalid task specified"}), 400

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

def handle_pipeline_decomposition(user_message):
    llm_input = generate_one_pipeline_decomposition_prompt(previous_messages[-2:], user_message)
    llm_output = send_llm_request_to_server(llm_input)
    pipeline_decomposition, pipeline_string = extract_pipeline_decomposition(llm_output)
    if pipeline_decomposition == {} or pipeline_decomposition == None:
        return {"generic_message": GENERIC_ERROR_MESSAGE }
    else:
        update_context_and_response(user_message, pipeline_decomposition, pipeline_string)
        return pipeline_decomposition
    
def handle_pipeline_decomposition_from_image(image_path):
    ocr_output = send_ocr_request_to_server(image_path)
    app.logger.info(f'{ocr_output=}')
    
    #pipeline_decomposition = build_pipeline_decomposition_from_ocr(texts)
    #pipeline_string = texts

    llm_input = generate_one_pipeline_decomposition_from_image_prompt(ocr_output)
    llm_output = send_llm_request_to_server(llm_input)
    pipeline_decomposition, pipeline_string = extract_pipeline_decomposition(llm_output)


    if pipeline_decomposition == {} or pipeline_decomposition == None:
        return {"generic_message": GENERIC_ERROR_MESSAGE }
    else:
        update_context_and_response('The user uploaded an image of a Pipeline', pipeline_decomposition, pipeline_string)
        return pipeline_decomposition


def handle_first_code_generation(user_message):
    app.logger.info("Handle First Code Generation")
    pipeline_decomposition = pipeline_decompositions[-1]
    #print(f'{pipeline_decomposition=}')
    for job in pipeline_decomposition['jobs']:
        #print(f'{job=}')
        llm_input = generate_first_code_generation_prompt(job, previous_messages[-2:], user_message=f"Generate the code for the following job : {job['name']}")
        response = send_llm_request_to_server(llm_input)
        code_string = extract_code_from_output(response)
        #print(f'{code_string=}')
        job['code'] = code_string
        job['cmd_line'] = f'''python job_{job['id']}.py'''
    create_python_files(pipeline_decomposition, APP_DIR)
    update_context_and_response(user_message, pipeline_decomposition, code_string)
    return pipeline_decomposition

def handle_iteration_on_code_generation(user_message):
    app.logger.info("Handle Iteration on Code Generation")
    pipeline_decomposition = pipeline_decompositions[-1]
    if len(pipeline_decomposition['jobs']) == 1:
        iteration_requests = [{'job_number': '1', 'is_concerned_by_user_request': True, 'adapted_request': user_message}]
    iteration_requests = determine_iteration_requests(pipeline_decomposition, user_message)
    nb_tries = 1

    # Repeat the analysis of the user requests if the number of Jobs analyzed is not correct
    while len(iteration_requests) != len(pipeline_decomposition['jobs']) and nb_tries <= 3:
        iteration_requests = determine_iteration_requests(pipeline_decomposition, user_message)
        nb_tries += 1

    app.logger.info(f'{iteration_requests=}')
    app.logger.info(f'{pipeline_decomposition=}')

    # If no iteration request is needed
    if not (True in [it_rq['is_concerned_by_user_request'] for it_rq in iteration_requests]):
        return {"generic_message": GENERIC_ERROR_MESSAGE }
    else:
        # For every Job in the Pipeline, check if there is an iteration request for this Job. If so, regenerate code.
        for iteration_request in iteration_requests:
            job = pipeline_decomposition['jobs'][int(iteration_request['job_number'])-1]
            if iteration_request['is_concerned_by_user_request']:
                user_message = iteration_request['adapted_request']
                llm_input = generate_iteration_on_code_generation_prompt(job=job, user_message=user_message)
                response = send_llm_request_to_server(llm_input)
                code_string = extract_code_from_output(response)
                job['code'] = code_string

        create_python_files(pipeline_decomposition, APP_DIR)
        update_context_and_response(user_message, pipeline_decomposition, code_string)
        return pipeline_decomposition

def determine_iteration_requests(pipeline_decomposition, user_message):
    try:
        llm_input = generate_determine_iteration_requests_prompt(pipeline_decomposition, user_message)
        llm_output = send_llm_request_to_server(llm_input)
        app.logger.info('Extracting iteration requests')
        iteration_requests, iteration_requests_string = extract_iteration_requests(llm_output)
        print(f'{iteration_requests=}')
    except Exception as e:
        print(e)
        iteration_requests = []
    
    return iteration_requests

def handle_saagie_creation():
    global pipeline_decompositions
    global previous_messages
    app.logger.info(f'{pipeline_decompositions[-1]=}')
    saagie, jobs, pipeline_id = create_pipeline_in_saagie(pipeline_decompositions[-1], SAAGIE_PLATFORM_URL, SAAGIE_PROJECT_ID, SAAGIE_USER_NAME, SAAGIE_USER_PASSWORD)
    previous_messages, pipeline_decompositions = reset_context(previous_messages, pipeline_decompositions)
    return {"result": "The pipeline and its Jobs were successfully created in Saagie."}

def send_llm_request_to_server(llm_input):
    response = requests.post(f'{LLM_SERVER_URL}/llm', json={'llm_input': llm_input}, verify=False)
    response.raise_for_status()
    return response.json().get('llm_output')

def send_ocr_request_to_server(file):
    files = {'file': file}
    response = requests.post(f'{LLM_SERVER_URL}/ocr', files=files, verify=False)
    response.raise_for_status()
    return response.json().get('ocr_output')

def update_context_and_response(user_message, pipeline_decomposition, response_string):
    pipeline_decompositions.append(pipeline_decomposition)
    previous_messages.append({'role': 'user', 'content': user_message})
    previous_messages.append({'role': 'assistant', 'content': response_string})

def reset_context(previous_messages, pipeline_decompositions):
    previous_messages = []
    pipeline_decompositions = []
    return previous_messages, pipeline_decompositions

def check_if_env_variables_are_set(variables):
    app.logger.info('Checking if env vars are set')
    missing_variables = [var for var in variables if var not in os.environ]
    #app.logger.info(missing_variables)
    if missing_variables:
        if len(missing_variables) == 1:
            error_message = f"The following environment variable is not set:\n\n"
            error_message += '\n'.join(missing_variables)
            error_message += "\n\nCreate it to make the app work properly."        
        else:
            error_message = f'''The following environment variables are not set:\n\n'''
            error_message += '\n'.join(missing_variables)
            error_message += "\n\nCreate them to make the app work properly."
        raise Exception(error_message)
    else:
        global LLM_SERVER_URL, SAAGIE_PLATFORM_URL, SAAGIE_PROJECT_ID, SAAGIE_USER_NAME, SAAGIE_USER_PASSWORD
        LLM_SERVER_URL = os.environ['LLM_SERVER_URL']
        SAAGIE_PLATFORM_URL = os.environ['SAAGIE_PLATFORM_URL']
        SAAGIE_PROJECT_ID = os.environ['SAAGIE_PROJECT_ID']
        SAAGIE_USER_NAME = os.environ['SAAGIE_USER_NAME']
        SAAGIE_USER_PASSWORD = os.environ['SAAGIE_USER_PASSWORD']
    
        return True

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
    