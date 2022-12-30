from typing import Any
from fastapi import APIRouter, Depends
from urllib.parse import unquote_plus
from src.controllers.ObjectStorageController import ObjectStorageController
from src.dependencies.authentication import validate_user

router = APIRouter(
    prefix="/datalake/objectstorage",
    tags=["datalake objectstorage"],
    responses={404: {"message": "Not found"}},
    dependencies=[Depends(validate_user)],
)


@router.get("")
def list_buckets() -> Any:
    """
    List all buckets in object storage.
    """

    return ObjectStorageController.list_buckets()


@router.get("/{bucket_name}")
def list_objects_in_bucket(*, bucket_name: str, obj_name: str = "") -> Any:
    """
    List all objects in bucket.
    """

    return ObjectStorageController.list_objects(
        unquote_plus(bucket_name), unquote_plus(obj_name)
    )
