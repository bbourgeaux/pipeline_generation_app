from flask import Flask, render_template, request, jsonify, Response
from mistral_utils_model import *
from saagieapi_utils_model import *
import json
import time
import requests

app = Flask(__name__)
#LLM_SERVER_URL = 'http://10.201.0.51:81'  # Replace with your LLM server's IP
LLM_SERVER_URL = 'http://10.201.0.61:80'  # Replace with your LLM server's IP
#model_name = "TheBloke/Mistral-7B-Instruct-v0.1-GPTQ"
#revision = "main"
#model, tokenizer = load_model(model_name, revision)
global previous_messages
previous_messages = []
pipeline_decompositions = []

@app.route('/', methods=['GET', 'POST'])
def chat():
    return render_template("index_model.html")

@app.route('/generate-response', methods=['POST'])
def generate_response():
    try:
        task = request.json.get('task', '')
        user_message = request.json.get('user_message', '')
            
        if task == 'pipeline_decomposition':
    
            llm_input = generate_one_pipeline_decomposition_prompt(previous_messages, user_message)
        
            # Send input to the LLM server
            response = requests.post(f'{LLM_SERVER_URL}/generate', json={'llm_input': llm_input})
            # Get the LLM's response
            llm_output = response.json().get('llm_output')
            print(f'{llm_output=}')
            print('Generation OK')
            pipeline_decomposition = extract_pipeline_decomposition(llm_output)
            print('Extraction OK')
            pipeline_decompositions.append(pipeline_decomposition)
            previous_messages.append({'role': 'user', 'content': user_message})
            previous_messages.append({'role': 'assistant', 'content': pipeline_decomposition})
            response = pipeline_decomposition
            
        elif task == 'code_generation':
            if user_message == '':
                user_message = 'Generate the codes please'
                pipeline_decomposition = pipeline_decompositions[-1]
                #print(f'{pipeline_decomposition=}')
                for job in pipeline_decomposition:
                    llm_input = generate_one_code_generation_prompt(job)

                    # Send input to the LLM server
                    response = requests.post(f'{LLM_SERVER_URL}/generate', json={'llm_input': llm_input})
                    # Get the LLM's response
                    llm_output = response.json().get('llm_output')
                    #print(f'{llm_output=}')
                    print('Generation OK')
                    job['code'] = extract_code_from_output(llm_output)
                    job['cmd_line'] = f'''python job_{job['id']}.py'''
                    print('Extraction OK')
                    
                    # Send each code individually
                    #yield jsonify({'response': job})
                    
                    
                create_python_files(pipeline_decomposition)
                pipeline_decompositions.append(pipeline_decomposition)
                previous_messages.append({'role': 'user', 'content': user_message})
                previous_messages.append({'role': 'assistant', 'content': pipeline_decomposition})

                response = pipeline_decompositions[-1]
                #pipeline_decomposition = pipeline_decompositions[-1]
                #response = Response(generate_code_responses(pipeline_decompositions[-1]), content_type='text/event-stream')
            #else:
                #pipeline_decomposition = pipeline_decompositions[-1]
                #llm_input = generate_whole_code_generation_prompt(previous_messages, user_message)
                #print(f'{llm_input=}')
                # Send input to the LLM server
                #response = requests.post(f'{LLM_SERVER_URL}/generate', json={'llm_input': llm_input})
                # Get the LLM's response
                #llm_output = response.json().get('llm_output')
                #print(f'{llm_output=}')
                #print('Generation OK')
                #pipeline_decomposition = extract_pipeline_decomposition(llm_output)
                #print('Extraction OK')
                #pipeline_decompositions.append(pipeline_decomposition)
                #previous_messages.append({'role': 'user', 'content': user_message})
                #previous_messages.append({'role': 'assistant', 'content': pipeline_decomposition})
                
                #response = pipeline_decompositions[-1]

        elif task == 'creation_in_saagie':
            saagie, jobs, pipeline_id = create_pipeline_in_saagie(pipeline_decompositions[-1])
            response = {"result":"The pipeline 'Pipeline by Mistral' and its Jobs were successfully created in Saagie."}
            
        return jsonify(response)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=5000)
