from typing import Any
from fastapi import APIRouter
from src.controllers.ObjectStorageController import ObjectStorageController

router = APIRouter(
    prefix="/datalake/objectstorage",
    tags=["datalake objectstorage"],
    responses={404: {"message": "Not found"}},
)


@router.get("")
def list_buckets() -> Any:
    """
    List all buckets in object storage.
    """

    return ObjectStorageController.list_buckets()


@router.get("/{bucket_name}")
def list_objects_in_bucket(*, bucket_name: str, obj_name: str = None) -> Any:
    """
    List all objects in bucket.
    """

    return ObjectStorageController.list_objects(bucket_name, obj_name)
