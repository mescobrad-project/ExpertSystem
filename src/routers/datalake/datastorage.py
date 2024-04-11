from typing import Any
from fastapi import APIRouter, Depends
from urllib.parse import unquote_plus
from src.controllers.DataStorageController import DataStorageController
from src.dependencies.authentication import validate_user

router = APIRouter(
    prefix="/datalake/datastorage",
    tags=["datalake datastorage"],
    responses={404: {"message": "Not found"}},
    # dependencies=[Depends(validate_user)],
)


@router.get("")
def list_catalogs() -> Any:
    """
    List all catalogs in data storage.
    """
    return DataStorageController.list_catalogs()


@router.get("/{catalog}")
def list_catalog_schemas(catalog: str) -> Any:
    """
    List all schemas in a catalog.
    """
    return DataStorageController.list_catalog_schemas(catalog)


@router.get("/{catalog}/{schema}")
def list_catalog_tables(catalog: str, schema: str) -> Any:
    """
    List all tables in a catalog schema.
    """
    return DataStorageController.list_catalog_tables(catalog, schema)


@router.get("/{catalog}/{schema}/{table}/describe")
def describe_catalogs(catalog: str, schema: str, table: str) -> Any:
    """
    Get table columns given a catalog schema.
    """
    return DataStorageController.describe_catalog_tables(catalog, schema, table)


@router.get("/{catalog}/{schema}/{table}/sources")
def list_catalog_table_sources(catalog: str, schema: str, table: str) -> Any:
    """
    Get table sources given a catalog schema.
    """
    return DataStorageController.list_catalog_table_sources(catalog, schema, table)


@router.get("/{catalog}/{schema}/{table}/{filename}/download")
def download_catalog_table_sources(
    catalog: str, schema: str, table: str, filename: str
) -> Any:
    """
    Download source given a catalog schema, table and source name.
    """
    return DataStorageController.download_catalog_table_sources(
        catalog, schema, table, filename
    )
