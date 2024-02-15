from joblib import Job

class Job_1(Job):
    def __init__(self):
        super().__init__()
        self.input_resources = ['example1.ext']
        self.output_resources = ['example2.ext']

    def run(self):
        # do something to generate example2.ext
        pass

class Job_2(Job):
    def __init__(self):
        super().__init__()
        self.input_resources = ['example2.ext']
        self.output_resources = ['example3.ext']

    def run(self):
        # do something to use example2.ext and generate example3.ext
        pass

class Job_3(Job):
    def __init__(self):
        super().__init__()
        self.input_resources = ['example3.ext']
        self.output_resources = ['example4.ext']

    def run(self):
        # do something to use example3.ext and generate example4.ext
        pass

# create a pipeline with the 3 jobs
pipeline = {"name": "My Pipeline", "description": "This Pipeline has 3 Jobs.",
           "jobs": [Job_1, Job_2, Job_3]}

# run the pipeline
run_pipeline(pipeline)