from src.clients.minio import client


class BaseController:
    def __init__(self, client):
        self.client = client

    def list_buckets(self):
        return self.client.list_buckets()

    def list_objects(self, bucket_name: str, obj_name: str = None):
        if self.client.bucket_exists(bucket_name):
            prefix = ""
            if obj_name:
                prefix = obj_name

            return self.client.list_objects(
                bucket_name, prefix=prefix, include_user_meta=True
            )

        return []


ObjectStorageController = BaseController(client)
