import uuid
from fastapi import Header
from typing import Any
from keycloak import KeycloakOpenID
from minio import Minio
import pytz, requests
from sqlalchemy import desc
from sqlalchemy.orm import Session
import xml.etree.ElementTree as ElementTree
from trino.dbapi import connect
from trino.auth import BasicAuthentication, JWTAuthentication
import json
from uuid import UUID
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
    QB_API_BASE_URL,
)
from src.schemas.NewRunSchema import Run, RunAction
from src.models._all import (
    NewRunModel,
    NewRunActionModel,
    NewWorkflowActionModel,
    NewWorkflowStepModel,
)

keycloak_openid = KeycloakOpenID(
    server_url=OAUTH_HOST,
    client_id=OAUTH_CLIENT_ID,
    realm_name=OAUTH_REALM,
    client_secret_key=OAUTH_CLIENT_SECRET,
    verify=True,
)


def get_variables(table: str, token: str):
    auth = JWTAuthentication(token)
    client = connect(
        host=TRINO_HOST,
        port=TRINO_PORT,
        http_scheme=TRINO_SCHEME,
        auth=auth,
        timezone=str(pytz.timezone("UTC")),
        # verify=False,
    )
    cursor = client.cursor()
    cursor.execute("SHOW SCHEMAS IN iceberg")
    buckets = cursor.fetchall()
    schema = buckets[0][0]
    query = f"SELECT DISTINCT(variable_name) FROM iceberg.{schema}.{table}"
    cursor.execute(query)
    result = cursor.fetchall()
    return result


def query_trino_table(
    ttable: str, vname: str, vvalue: str, token: str = Header()
) -> Any:
    auth = JWTAuthentication(token)
    client = connect(
        host=TRINO_HOST,
        port=TRINO_PORT,
        http_scheme=TRINO_SCHEME,
        auth=auth,
        timezone=str(pytz.timezone("UTC")),
        # verify=False,
    )
    cursor = client.cursor()
    cursor.execute("SHOW SCHEMAS IN iceberg")
    buckets = cursor.fetchall()
    schema = buckets[0][0]
    query = f"SELECT DISTINCT(source) FROM iceberg.{schema}.{ttable}"
    if vname != "":
        query += f" WHERE variable_name = '{vname}' "
    if vname != "" and vvalue != "":
        query += f" AND variable_value = '{vvalue}' "
    cursor.execute(query)
    result = cursor.fetchall()
    return result


def get_trino_schema(token: str) -> Any:
    auth = JWTAuthentication(token)
    client = connect(
        host=TRINO_HOST,
        port=TRINO_PORT,
        http_scheme=TRINO_SCHEME,
        auth=auth,
        timezone=str(pytz.timezone("UTC")),
        # verify=False,
    )
    cursor = client.cursor()
    cursor.execute("SHOW SCHEMAS IN iceberg")
    buckets = cursor.fetchall()
    return buckets[0][0]


def get_trino_tables(token: str) -> Any:
    auth = JWTAuthentication(token)
    client = connect(
        host=TRINO_HOST,
        port=TRINO_PORT,
        http_scheme=TRINO_SCHEME,
        auth=auth,
        timezone=str(pytz.timezone("UTC")),
        # verify=False,
    )
    cursor = client.cursor()
    cursor.execute("SHOW SCHEMAS IN iceberg")
    buckets = cursor.fetchall()
    cursor.execute(f"SHOW TABLES IN iceberg.{buckets[0][0]}")
    tables = cursor.fetchall()

    return tables


def get_buckets_from_minio(token: str) -> Any:
    minio_url = f"https://{S3_ENDPOINT}"
    minio_data = {
        "Action": "AssumeRoleWithWebIdentity",
        "Version": "2011-06-15",
        "WebIdentityToken": token,
    }

    response = requests.post(minio_url, data=minio_data)
    xml_data = ElementTree.fromstring(response.text)

    # Step 2: Parse the output to extract the credentials
    access_key = xml_data.find(
        ".//{https://sts.amazonaws.com/doc/2011-06-15/}AccessKeyId"
    ).text
    secret_access_key = xml_data.find(
        ".//{https://sts.amazonaws.com/doc/2011-06-15/}SecretAccessKey"
    ).text
    session_token = xml_data.find(
        ".//{https://sts.amazonaws.com/doc/2011-06-15/}SessionToken"
    ).text

    client = Minio(
        endpoint=S3_ENDPOINT,
        access_key=access_key,
        secret_key=secret_access_key,
        session_token=session_token,
        # For local testing
        # secure=False,
    )
    buckets = client.list_buckets()
    return buckets


def get_files_from_minio(bucket_name: str, x_es_token: str = Header()) -> Any:
    minio_url = S3_ENDPOINT
    minio_data = {
        "Action": "AssumeRoleWithWebIdentity",
        "Version": "2011-06-15",
        "WebIdentityToken": x_es_token,
    }

    response = requests.post(minio_url, data=minio_data)
    xml_data = ElementTree.fromstring(response.text)

    # Step 2: Parse the output to extract the credentials
    access_key = xml_data.find(
        ".//{https://sts.amazonaws.com/doc/2011-06-15/}AccessKeyId"
    ).text
    secret_access_key = xml_data.find(
        ".//{https://sts.amazonaws.com/doc/2011-06-15/}SecretAccessKey"
    ).text
    session_token = xml_data.find(
        ".//{https://sts.amazonaws.com/doc/2011-06-15/}SessionToken"
    ).text

    client = Minio(
        endpoint=S3_ENDPOINT,
        access_key=access_key,
        secret_key=secret_access_key,
        session_token=session_token,
        secure=False,
    )
    files = client.list_objects(bucket_name)
    return files


def get_file_from_minio(
    bucket_name: str, file_name: str, x_es_token: str = Header()
) -> Any:
    minio_url = S3_ENDPOINT
    minio_data = {
        "Action": "AssumeRoleWithWebIdentity",
        "Version": "2011-06-15",
        "WebIdentityToken": x_es_token,
    }

    response = requests.post(minio_url, data=minio_data)
    xml_data = ElementTree.fromstring(response.text)

    # Step 2: Parse the output to extract the credentials
    access_key = xml_data.find(
        ".//{https://sts.amazonaws.com/doc/2011-06-15/}AccessKeyId"
    ).text
    secret_access_key = xml_data.find(
        ".//{https://sts.amazonaws.com/doc/2011-06-15/}SecretAccessKey"
    ).text
    session_token = xml_data.find(
        ".//{https://sts.amazonaws.com/doc/2011-06-15/}SessionToken"
    ).text

    client = Minio(
        endpoint=S3_ENDPOINT,
        access_key=access_key,
        secret_key=secret_access_key,
        session_token=session_token,
        secure=False,
    )
    file = client.get_object(bucket_name, file_name)

    return file


def createRun(db: Session, data: Run, ws_id: int) -> Any:
    run = {
        "id": uuid.uuid4(),
        "workflow_id": data.workflow_id,
        "title": data.title,
        "notes": data.notes,
        "ws_id": ws_id,
        "is_part_of_other": data.is_part_of_other,
        "json_representation": data.json_representation,
        "step": data.step,
        "action": data.action,
        "status": data.status,
    }
    db.execute(NewRunModel.__table__.insert().values(run))
    db.commit()
    return run


def saveAction(db: Session, data: RunAction, id: str = None) -> Any:
    action = {
        "id": uuid.uuid4() if id is None else id,
        "action_id": data.action_id,
        "action_type": data.action_type,
        "input": data.input,
        "value": data.value,
        "status": data.status,
        "ws_id": data.ws_id,
        "run_id": data.run_id,
    }
    if id is not None and id != "":
        db.execute(
            NewRunActionModel.__table__.update()
            .where(NewRunActionModel.id == id)
            .values(action)
        )
    else:
        db.execute(NewRunActionModel.__table__.insert().values(action))
    db.commit()
    return action


def getActions(db: Session, run_id: str) -> Any:
    actions = db.execute(
        NewRunActionModel.__table__.select().where(NewRunActionModel.run_id == run_id)
    ).fetchall()
    return actions


def getAction(db: Session, action_id: str) -> Any:
    action = (
        db.query(NewRunActionModel).filter(NewRunActionModel.id == action_id).first()
    )

    return action


def completeAction(db: Session, action_id: str) -> Any:
    action = (
        db.execute(
            NewRunActionModel.__table__.select().where(
                NewRunActionModel.id == action_id
            )
        )
        .fetchone()
        ._mapping
    )
    db.execute(
        NewRunActionModel.__table__.update()
        .where(NewRunActionModel.id == action_id)
        .values({"status": "completed"})
    )
    db.commit()
    return action


def get_data_from_querybuilder(db: Session, run_id: str, action_id: str, data: dict):
    action = (
        db.query(NewRunActionModel).filter(NewRunActionModel.id == action_id).first()
    )
    db.execute(
        NewRunActionModel.__table__.update()
        .where(NewRunActionModel.id == action_id)
        .values({"value": json.dumps(data)})
    )
    db.commit()
    return action


def getActionInputForQueryBuilder(
    db: Session, action_id: str, workflow_id: str, token: str
) -> Any:
    run = (
        db.execute(NewRunModel.__table__.select().where(NewRunModel.id == workflow_id))
        .fetchone()
        ._mapping
    )
    action = (
        db.execute(
            NewRunActionModel.__table__.select().where(
                NewRunActionModel.id == action_id
            )
        )
        .fetchone()
        ._mapping
    )
    waction = (
        db.execute(
            NewWorkflowActionModel.__table__.select().where(
                NewWorkflowActionModel.id == action["action_id"]
            )
        )
        .fetchone()
        ._mapping
    )

    input = json.loads(action["input"])
    trino_files = []
    datalake_files = []
    for key in input:
        if "bucket" in key:
            datalake_files.append({"bucket": key["bucket"], "file": key["file"]})
    for key in input:
        if "table" in key and key["file"].endswith(".csv"):
            trino_files.append(
                {
                    "catalog": "iceberg",
                    "schema_": key["schema"],
                    "table": key["table"],
                    "name": key["name"],
                    "selected": True,
                    "file": key["file"],
                }
            )

    return {
        "step": {
            "id": action["id"],
            "number": waction["order"],
            "start": action["created_at"],
            "finish": "",
            "sid": action["action_id"],
            "name": waction["name"],
            "metadata": {
                "url": f"{QB_API_BASE_URL}/{workflow_id}/{action_id}",
                "workflow_id": run["workflow_id"],
                "run_id": action["run_id"],
                "data_use": {"trino": trino_files, "datalake": datalake_files},
                "base_save_path": {
                    "bucket_name": "common",
                    "object_name": f"workflows/{workflow_id}",
                },
            },
            "completed": action["value"] is not None and action["value"] != "",
        },
        "completed": False,
    }


def get_all_runs(
    db: Session,
    ws_id: int,
    workflow_id: UUID | None = None,
    skip: int = 0,
    limit: int = 20,
) -> Any:
    runs = (
        db.query(NewRunModel)
        .filter(
            NewRunModel.ws_id == int(ws_id)
            and (workflow_id == None or NewRunModel.workflow_id == workflow_id)
        )
        .order_by(desc(NewRunModel.created_at))
        .slice(skip, skip + limit)
        .all()
    )

    return runs


def get_run(db: Session, ws_id: int, run_id: UUID) -> Any:
    run = db.query(NewRunModel).filter(NewRunModel.id == str(run_id)).first()
    run.actions = (
        db.query(NewRunActionModel)
        .filter(NewRunActionModel.run_id == str(run.id))
        .all()
    )
    return run


def get_run_actions(db: Session, ws_id: int, run_id: UUID) -> Any:
    run = (
        db.query(NewRunModel)
        .filter(NewRunModel.ws_id == ws_id and NewRunModel.id == run_id)
        .first()
    )
    run.actions = (
        db.query(NewRunActionModel).filter(NewRunActionModel.run_id == run.id).all()
    )
    return run.actions


def get_action(db: Session, ws_id: int, run_id: UUID, action_id: UUID) -> Any:
    action = (
        db.query(NewRunActionModel)
        .filter(
            NewRunActionModel.ws_id == ws_id
            and NewRunActionModel.run_id == run_id
            and NewRunActionModel.id == action_id
        )
        .first()
    )
    return action


def get_action_by_id(db: Session, action_id: UUID) -> Any:
    action = (
        db.query(NewRunActionModel).filter(NewRunActionModel.id == action_id).first()
    )
    return action


def next_step(db: Session, run_id: UUID) -> Any:
    run = db.query(NewRunModel).filter(NewRunModel.id == run_id).first()
    run.step = int(run.step) + 1
    db.commit()
    return run


def complete_run(db: Session, run_id: UUID) -> Any:
    run = db.query(NewRunModel).filter(NewRunModel.id == run_id).first()
    run.status = "completed"
    db.commit()
    return run


def get_workflow_variable_names(db: Session, workflow_id: UUID) -> Any:
    res = (
        db.execute(
            "SELECT DISTINCT(variable) as variable FROM new_workflow_action_conditionals WHERE workflow_action_id IN (SELECT id FROM new_workflow_actions WHERE workflow_id = :workflow_id)",
            {"workflow_id": str(workflow_id)},
        )
        .fetchall()
        ._mapping
    )
    return res
