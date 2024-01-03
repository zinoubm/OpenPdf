from app.core.config import settings
import boto3


class AwsS3Manager:
    def __init__(self):
        self.bucket_name = settings.AWS_BUCKET_NAME

        self.session = boto3.Session(
        aws_access_key_id=settings.ACCESS_KEY_ID,
        aws_secret_access_key=settings.SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION,
        )
        self.s3_client = self.session.client("s3")

    def download_s3_object(self, object_key, dest_folder = 'tmp'):
        dest_path = f'/{dest_folder}/{object_key.split("/")[-1]}'

        try:
            self.s3_client.download_file(self.bucket_name, object_key, dest_path)
        except Exception as e:
            print(f"Error downloading {object_key} from S3: {e}")
            return None

        return dest_path


    def upload_s3_object(self):
        pass

aws_s3_manager = AwsS3Manager()