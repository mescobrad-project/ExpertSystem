from minio import Minio
from src.config import S3_ENDPOINT, S3_ACCESS_KEY_ID, S3_SECRET_ACCESS_KEY

client = Minio(
    endpoint=S3_ENDPOINT,
    access_key=S3_ACCESS_KEY_ID,
    secret_key=S3_SECRET_ACCESS_KEY,
)
