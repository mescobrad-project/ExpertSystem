from typing import Any
from fastapi import APIRouter, Depends
from urllib.parse import unquote_plus
from src.controllers.ObjectStorageController import ObjectStorageController
from src.dependencies.authentication import validate_user

router = APIRouter(
    prefix="/datalake/objectstorage",
    tags=["datalake objectstorage"],
    responses={404: {"message": "Not found"}},
    # dependencies=[Depends(validate_user)],
)


@router.get("")
def list_buckets() -> Any:
    """
    List all buckets in object storage.
    """

    return ObjectStorageController.list_buckets()


@router.get("/list/{bucket_name}")
def list_objects_in_bucket(*, bucket_name: str, obj_name: str = "") -> Any:
    """
    List all objects in bucket.
    """

    return ObjectStorageController.list_objects(
        unquote_plus(bucket_name), unquote_plus(obj_name)
    )


@router.get("/get/{bucket_name}")
def get_object_in_bucket(*, bucket_name: str, obj_name: str = "") -> Any:
    """
    Get an object in bucket.
    """

    return ObjectStorageController.get_object(
        unquote_plus(bucket_name), unquote_plus(obj_name)
    )


@router.get("/info/{bucket_name}")
def stat_object_in_bucket(*, bucket_name: str, obj_name: str = "") -> Any:
    """
    Get info of an object in bucket.
    """

    return ObjectStorageController.stat_object(
        unquote_plus(bucket_name), unquote_plus(obj_name)
    )
