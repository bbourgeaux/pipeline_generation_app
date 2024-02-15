from saagieapi import *
import os

def create_pipeline_in_saagie(pipeline, saagie_platform_url, saagie_project_id, saagie_user_name, saagie_user_password):    
    # Connect to API
    saagie = SaagieApi.easy_connect(url_saagie_platform=saagie_platform_url,
                                    user=saagie_user_name,
                                    password=saagie_user_password)
    
    from gql import gql

    import logging
    import sys

    import requests
    from requests import ConnectionError as requestsConnectionError
    from requests import HTTPError, RequestException, Timeout

    class BearerAuth(requests.auth.AuthBase):
        def __init__(self, realm: str, url: str, platform: str, login: str, password: str):
            self._realm = realm
            self._url = url
            self._platform = platform
            self._login = login
            self._password = password
            self.token = self._authenticate(realm, url, login, password)

        def refresh_token(self):
            self.token = self._authenticate(self._realm, self._url, self._login, self._password)

        def __call__(self, req):
            req.headers["authorization"] = f"Bearer {self.token}"
            return req

        @staticmethod
        def _authenticate(realm: str, url: str, login: str, password: str) -> str:
            """
            Retrieve a Bearer connection token
            :param realm: platform url prefix (eg: saagie)
            :param url: platform URL (eg: https://saagie-workspace.prod.saagie.io)
            :param login: username to log in with
            :param password: password to log in with
            :return: a token
            """
            try:
                session = requests.session()
                session.headers["Content-Type"] = "application/json"
                session.headers["Saagie-Realm"] = realm
                response = session.post(
                    f"{url}/authentication/api/open/authenticate",
                    json={"login": login, "password": password},
                    verify=False,
                )
                response.raise_for_status()
                return response.text
            except (HTTPError, requestsConnectionError, Timeout, RequestException) as err:
                logging.error(err)
                sys.exit(1)
        
    def create_graph(project_id,
                graph_pipeline,
                name,
                description,
                alias,
                release_note=None):
        
        if not graph_pipeline.list_job_nodes:
            graph_pipeline.to_pipeline_graph_input()

        params = {
            "name": name,
            "alias": alias,
            "description": description,
            "projectId": project_id,
            "releaseNote": release_note,
            "jobNodes": graph_pipeline.list_job_nodes,
            "conditionNodes": graph_pipeline.list_conditions_nodes,
            "isScheduled":False,
        }


        GQL_CREATE_GRAPH_PIPELINE = """
        mutation createGraphPipelineMutation($name: String!, 
                                                            $description: String, 
                                            $projectId: UUID!,
                                                                $releaseNote: String, 
                                            $alerting: JobPipelineAlertingInput,
                                            $isScheduled: Boolean!, 
                                            $cronScheduling: Cron, 
                                            $scheduleTimezone:TimeZone,
                                            $jobNodes: [JobNodeInput!], 
                                            $conditionNodes: [ConditionNodeInput!],
                                            $alias: String!) {
            createGraphPipeline(pipeline:    {
                name: $name
                description: $description
                projectId: $projectId
                releaseNote : $releaseNote
                alerting: $alerting
                isScheduled: $isScheduled
                cronScheduling: $cronScheduling
                scheduleTimezone: $scheduleTimezone
                graph: {
                    jobNodes: $jobNodes
                    conditionNodes: $conditionNodes
                }
                alias: $alias
                
            }
            ) {
                id
            }
        }
        """

        auth = BearerAuth(
            realm=saagie.realm, url=saagie.url_saagie, platform=1, login=saagie_user_name, password=saagie_user_password
        )
        logging.info("✅ Successfully connected to your platform %s", saagie.url_saagie)
        url_api = f"{saagie.url_saagie}projects/api/platform/1/graphql"
        #client = GqlClient(auth=auth, api_endpoint=url_api, retries=0)
        from gql.transport.requests import RequestsHTTPTransport
        from gql import Client
        transport = RequestsHTTPTransport(
            url=url_api, auth=auth, use_json=True, verify=False, retries=0, timeout=10
        )
        client = Client(transport=transport, fetch_schema_from_transport=True)



        result = client.execute(document=gql(GQL_CREATE_GRAPH_PIPELINE), variable_values=params, upload_files=False)
        logging.info("✅ Pipeline [%s] successfully created", name)
        return result
        # Create the jobs

    # Create the jobs
    for job in pipeline['jobs']:
        # Create a Python job inside the project
        job_dict = saagie.jobs.create(
            # job_name=job['name'],
            job_name=f'''[{pipeline['name']}] - {job['name']}''',
            project_id=saagie_project_id,
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
    for job in pipeline['jobs']:
        job['saagie_job_node'] = JobNode(job['saagie_job_id'])
        
    # This part is only valid for a PIPELINE not a SINGLE JOB
    if len(pipeline['jobs']) == 1:
        pipeline_id = None
    else:
        # Create the dependencies between pipeline['jobs']
        root_job_id = None
        for job in pipeline['jobs']:
            dep = job['dep']
            if dep != 0:         
                previous_job = [job for job in pipeline['jobs'] if job['id'] == dep][0] # Get the previous job
                previous_job['saagie_job_node'].add_next_node(job['saagie_job_node']) # Indicates that the job "previous_job" is followed by "job".
            elif root_job_id == None:
                root_job_id = job['id']

        # Create the pipeline
        graph_pipeline = GraphPipeline()
        graph_pipeline.add_root_node([job for job in pipeline['jobs'] if job['id'] == root_job_id][0]['saagie_job_node']) # Indicates the pipeline will start with job_node1
        #pipeline_id = saagie.pipelines.create_graph(
        pipeline_id = create_graph(
            project_id=saagie_project_id,
            graph_pipeline=graph_pipeline,
            name=pipeline['name'],
            alias=pipeline['name'].replace(' ','_'),
            description=pipeline['description'], 
        )['createGraphPipeline']['id']

    return saagie, pipeline, pipeline_id

def run_pipeline_in_saagie(saagie, pipeline_id):
    pipeline_final_state = saagie.pipelines.run_with_callback(pipeline_id=pipeline_id)
    return pipeline_final_state

def delete_pipeline_in_saagie(saagie, pipeline, pipeline_id):
    # Delete the Pipeline
    saagie.pipelines.delete(pipeline_id=pipeline_id)
    # Delete the Jobs
    for job in pipeline['jobs']:
        saagie.pipeline['jobs'].delete(job_id=job['saagie_job_id'])