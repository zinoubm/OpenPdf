import os
import boto3
from app.core.config import settings
from itertools import chain

class AwsBatchManager():
    def __init__(self) -> None:
        self.job_queue = settings.AWS_BATCH_JOB_QUEUE_ARN
        self.job_definition = settings.AWS_BATCH_JOB_DEFINITION_ARN

        self.session = boto3.Session(
        aws_access_key_id=settings.ACCESS_KEY_ID,
        aws_secret_access_key=settings.SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION,
        )

        self.client = self.session.client("batch")
        

    def run(self, payload ,job_name='process_openpdfai_document', worker_file_path='app/worker.py'):
        
        params = [[f"--{key}" ,value] for key, value in payload.items()]

        try:
            response = self.client.submit_job(
            jobName=job_name,
            jobQueue=self.job_queue,
            jobDefinition=self.job_definition,
            containerOverrides={
                "command":[
                    "python",
                    worker_file_path,
                ] + list(chain.from_iterable(params))
            }
        )
                        
        except Exception as e:
            return {"failed":1, "error":e}

        return response
    
aws_batch_manager = AwsBatchManager()
