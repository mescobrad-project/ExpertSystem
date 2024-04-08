from datetime import timedelta
from io import BytesIO
from src.clients.minio import client


class BaseController:
    def __init__(self, client):
        self.client = client

    def _bucket_exists(self, bucket_name: str):
        return self.client.bucket_exists(bucket_name)

    def _file_exists(self, bucket_name: str, obj_name: str):
        try:
            return self.client.stat_object(bucket_name, obj_name)
        except:
            return False

    def list_buckets(self):
        return self.client.list_buckets()

    def list_objects(self, bucket_name: str, obj_name: str = ""):
        if not self._bucket_exists(bucket_name):
            return []

        prefix = ""
        if obj_name != "":
            prefix = obj_name

        return self.client.list_objects(
            bucket_name, prefix=prefix, include_user_meta=True
        )

    def get_object(self, bucket_name: str, obj_name: str):
        if not self._bucket_exists(bucket_name):
            return None

        if not self._file_exists(bucket_name, obj_name):
            return None

        data = None
        try:
            response = self.client.get_object(bucket_name, obj_name)

            data = response.data
        finally:
            response.close()
            response.release_conn()

        return data

    def get_object_url(
        self, bucket_name: str, obj_name: str, expiration_in_minutes: int = 3
    ):
        if not self._bucket_exists(bucket_name):
            return None

        if not self._file_exists(bucket_name, obj_name):
            return None

        return self.client.get_presigned_url(
            method="GET",
            bucket_name=bucket_name,
            object_name=obj_name,
            expires=timedelta(minutes=expiration_in_minutes),
        )

    def stat_object(self, bucket_name: str, obj_name: str):
        if not self._bucket_exists(bucket_name):
            return None

        return self._file_exists(bucket_name, obj_name)

    def put_object(self, bucket_name: str, obj_name: str, data: bytes):
        if not self._bucket_exists(bucket_name):
            return None

        if self._file_exists(bucket_name, obj_name):
            return None

        return self.client.put_object(bucket_name, obj_name, BytesIO(data), len(data))


ObjectStorageController = BaseController(client)
