from flask import Flask, render_template, request, jsonify
import requests
import os
import urllib3
from llm_utils import (
    generate_one_pipeline_decomposition_prompt,
    extract_pipeline_decomposition,
    generate_one_code_generation_prompt,
    extract_code_from_output,
    create_python_files
)
from saagieapi_utils import create_pipeline_in_saagie

app = Flask(__name__)

LLM_SERVER_URL = os.environ['LLM_SERVER_URL']

# Remove a particular warning regarding Certificate Verification (HTTPS requests)
urllib3.disable_warnings(urllib3.exceptions.SubjectAltNameWarning)

previous_messages = []
pipeline_decompositions = []
current_task = None

@app.route('/', methods=['GET', 'POST'])
def chat():
    return render_template("index.html")

@app.route('/generate-response', methods=['POST'])
def generate_response():
    try:
        task = request.json.get('task', '')
        user_message = request.json.get('user_message', '')

        if task == 'pipeline_decomposition':
            pipeline_decomposition_response = handle_pipeline_decomposition(user_message)
            return jsonify(pipeline_decomposition_response)

        elif task == 'first_code_generation':
            code_generation_response = handle_code_generation(user_message)
            return jsonify(code_generation_response)
        
        elif task == 'iteration_on_code_generation':
            code_generation_response = handle_code_generation(user_message)
            return jsonify(code_generation_response)

        elif task == 'creation_in_saagie':
            saagie_creation_response = handle_saagie_creation()
            return jsonify(saagie_creation_response)

        else:
            return jsonify({"error": "Invalid task specified"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def handle_pipeline_decomposition(user_message):
    llm_input = generate_one_pipeline_decomposition_prompt(previous_messages, user_message)
    response = send_request_to_llm(llm_input)
    pipeline_decomposition = extract_pipeline_decomposition(response)
    print(f'''Extracted Pipeline Decomposition' : {pipeline_decomposition}''')
    update_context_and_response(user_message, pipeline_decomposition)
    return pipeline_decomposition

def handle_code_generation(user_message):
    user_message = user_message or 'Generate the codes please'
    pipeline_decomposition = pipeline_decompositions[-1]
    for job in pipeline_decomposition['jobs']:
        llm_input = generate_one_code_generation_prompt(job)
        response = send_request_to_llm(llm_input)
        job['code'] = extract_code_from_output(response)
        job['cmd_line'] = f'''python job_{job['id']}.py'''
    create_python_files(pipeline_decomposition)
    update_context_and_response(user_message, pipeline_decomposition)
    return pipeline_decomposition

def handle_saagie_creation():
    saagie, jobs, pipeline_id = create_pipeline_in_saagie(pipeline_decompositions[-1])
    return {"result": "The pipeline and its Jobs were successfully created in Saagie."}

def send_request_to_llm(llm_input):
    #response = requests.post(f'{LLM_SERVER_URL}/generate', json={'llm_input': llm_input}, verify='server.crt')
    response = requests.post(f'{LLM_SERVER_URL}/generate', json={'llm_input': llm_input}, verify=False)
    response.raise_for_status()
    return response.json().get('llm_output')

def update_context_and_response(user_message, pipeline_decomposition):
    pipeline_decompositions.append(pipeline_decomposition)
    previous_messages.append({'role': 'user', 'content': user_message})
    previous_messages.append({'role': 'assistant', 'content': pipeline_decomposition})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
    