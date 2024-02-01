from saagieapi import *

def create_pipeline_in_saagie(jobs):
    # Create the jobs
    SAAGIE_PLATFORM_URL = "https://research-workspace.pcv.saagie.io/projects/platform/1/"
    SAAGIE_USER_NAME = "baptiste.bourgeaux"
    SAAGIE_USER_PASSWORD = "SAAGIEboss24$"
    SAAGIE_PROJECT_ID = "32001cad-59ec-4c8b-8523-a778de6e1bcd"
    # Connect to API
    saagie = SaagieApi.easy_connect(url_saagie_platform=SAAGIE_PLATFORM_URL,
                                    user=SAAGIE_USER_NAME,
                                    password=SAAGIE_USER_PASSWORD)
    
    for job in jobs:
        # Create a Python job inside the project
        job_dict = saagie.jobs.create(
            job_name=job['name'],
            project_id=SAAGIE_PROJECT_ID,
            file=job['python_file_path'],
            description=job['description'],
            runtime_version='3.9',
            #command_line=f'''python job_{job['id']}.py'''
            command_line=job['cmd_line']
        )
        # Save the saagie_job_id in the 'jobs' variable
        job_id = job_dict['data']['createJob']['id']
        job['saagie_job_id'] = job_id
    
    # Create the Job Nodes
    for job in jobs:
        job['saagie_job_node'] = JobNode(job['saagie_job_id'])
        
    # This part is only valid for a PIPELINE not a SINGLE JOB
    if len(jobs) == 1:
        pipeline_id = None
    else:
        # Create the dependencies between Jobs
        root_job_id = None
        for job in jobs:
            dep = job['dep']
            if dep != 0:         
                previous_job = [job for job in jobs if job['id'] == dep][0] # Get the previous job
                previous_job['saagie_job_node'].add_next_node(job['saagie_job_node']) # Indicates that the job "previous_job" is followed by "job".
            elif root_job_id == None:
                root_job_id = job['id']

        # Create the pipeline
        graph_pipeline = GraphPipeline()
        graph_pipeline.add_root_node([job for job in jobs if job['id'] == root_job_id][0]['saagie_job_node']) # Indicates the pipeline will start with job_node1
        pipeline_id = saagie.pipelines.create_graph(
            project_id=SAAGIE_PROJECT_ID,
            graph_pipeline=graph_pipeline,
            name="Pipeline by Mistral",
            description="This pipeline was created by Mistral 7b."
        )['createGraphPipeline']['id']

    return saagie, jobs, pipeline_id

def run_pipeline_in_saagie(saagie, pipeline_id):
    pipeline_final_state = saagie.pipelines.run_with_callback(pipeline_id=pipeline_id)
    return pipeline_final_state

def delete_pipeline_in_saagie(saagie, jobs, pipeline_id):
    # Delete the Pipeline
    saagie.pipelines.delete(pipeline_id=pipeline_id)
    # Delete the Jobs
    for job in jobs:
        saagie.jobs.delete(job_id=job['saagie_job_id'])
    