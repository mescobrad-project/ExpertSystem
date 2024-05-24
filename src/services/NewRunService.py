from fastapi import Header
from typing import Any
from keycloak import KeycloakOpenID
from minio import Minio
import pytz, requests
import xml.etree.ElementTree as ElementTree
from trino.dbapi import connect
from trino.auth import BasicAuthentication, JWTAuthentication
from src.config import (
    OAUTH_HOST,
    OAUTH_CLIENT_SECRET,
    OAUTH_CLIENT_ID,
    OAUTH_CALLBACK_URL,
    OAUTH_REALM,
    OAUTH_LOGIN_SCOPE,
    S3_ACCESS_KEY_ID,
    S3_ENDPOINT,
    S3_SECRET_ACCESS_KEY,
    TRINO_HOST,
    TRINO_PORT,
    TRINO_SCHEME,
)

keycloak_openid = KeycloakOpenID(
        server_url=OAUTH_HOST,
        client_id=OAUTH_CLIENT_ID,
        realm_name=OAUTH_REALM,
        client_secret_key=OAUTH_CLIENT_SECRET,
        verify=True,
    )






def execute_sql_on_trino(sql: str, schema: str, catalog: str, x_es_token: str = Header()) -> Any:
    client = connect(
            host=TRINO_HOST,
            port=TRINO_PORT,
            http_scheme=TRINO_SCHEME,
            auth=JWTAuthentication(x_es_token),
            timezone=str(pytz.getTimezone("UTC")),
            verify=False,
        )
    cursor = client.cursor()
    cursor.execute(f"USE iceberg")
    cursor.execute(f"USE {schema}") # name of the bucket // Initial is the name of the organization
    cursor.execute(sql) # catalog.schema.table, no schemas in schemas tabls is a folder structure inside schema
    return cursor.fetchall()

def get_buckets_from_minio(bucket_name: str, x_es_token: str = Header()) -> Any:
    minio_url = S3_ENDPOINT
    minio_data = {
        "Action": "AssumeRoleWithWebIdentity",
        "Version": "2011-06-15",
        "WebIdentityToken": x_es_token
    }

    response = requests.post(minio_url, data=minio_data)
    xml_data = ElementTree.fromstring(response.text)

    # Step 2: Parse the output to extract the credentials
    access_key = xml_data.find('.//{https://sts.amazonaws.com/doc/2011-06-15/}AccessKeyId').text
    secret_access_key = xml_data.find('.//{https://sts.amazonaws.com/doc/2011-06-15/}SecretAccessKey').text
    session_token = xml_data.find('.//{https://sts.amazonaws.com/doc/2011-06-15/}SessionToken').text
    
    client = Minio(
        endpoint=S3_ENDPOINT,
        access_key=access_key,
        secret_key=secret_access_key,
        session_token=session_token,
        secure=False,
    )
    buckets = client.list_buckets(bucket_name)
    return buckets

def get_files_from_minio(bucket_name: str, x_es_token: str = Header()) -> Any:
    minio_url = S3_ENDPOINT
    minio_data = {
        "Action": "AssumeRoleWithWebIdentity",
        "Version": "2011-06-15",
        "WebIdentityToken": x_es_token
    }

    response = requests.post(minio_url, data=minio_data)
    xml_data = ElementTree.fromstring(response.text)

    # Step 2: Parse the output to extract the credentials
    access_key = xml_data.find('.//{https://sts.amazonaws.com/doc/2011-06-15/}AccessKeyId').text
    secret_access_key = xml_data.find('.//{https://sts.amazonaws.com/doc/2011-06-15/}SecretAccessKey').text
    session_token = xml_data.find('.//{https://sts.amazonaws.com/doc/2011-06-15/}SessionToken').text
    
    client = Minio(
        endpoint=S3_ENDPOINT,
        access_key=access_key,
        secret_key=secret_access_key,
        session_token=session_token,
        secure=False,
    )
    files = client.list_objects(bucket_name)
    return files
            
def get_file_from_minio(bucket_name: str, file_name: str, x_es_token: str = Header()) -> Any:
    minio_url = S3_ENDPOINT
    minio_data = {
        "Action": "AssumeRoleWithWebIdentity",
        "Version": "2011-06-15",
        "WebIdentityToken": x_es_token
    }

    response = requests.post(minio_url, data=minio_data)
    xml_data = ElementTree.fromstring(response.text)

    # Step 2: Parse the output to extract the credentials
    access_key = xml_data.find('.//{https://sts.amazonaws.com/doc/2011-06-15/}AccessKeyId').text
    secret_access_key = xml_data.find('.//{https://sts.amazonaws.com/doc/2011-06-15/}SecretAccessKey').text
    session_token = xml_data.find('.//{https://sts.amazonaws.com/doc/2011-06-15/}SessionToken').text
    
    client = Minio(
        endpoint=S3_ENDPOINT,
        access_key=access_key,
        secret_key=secret_access_key,
        session_token=session_token,
        secure=False,
    )
    file = client.get_object(bucket_name, file_name)
    
    return file
