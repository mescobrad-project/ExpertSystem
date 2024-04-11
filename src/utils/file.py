from datetime import datetime, timezone
from sqlalchemy.orm import Session
from src.controllers.FileController import FileController
from src.schemas.FileSchema import FileCreate


def save_object_storage_to_files(
    db: Session, ws_id: str, bucket_name: str, object_name: str, data
):
    name = object_name.split("/")[-1]

    object_name = (
        object_name.replace("/", " ")
        .replace("-", " ")
        .replace("_", " ")
        .replace(".", " ")
    )
    search = f"{bucket_name} {object_name}"

    FileController.create(
        db=db,
        obj_in=FileCreate(
            name=f"{name} {datetime.now(tz=timezone.utc).isoformat()}",
            ws_id=ws_id,
            search=search,
            info=data,
        ),
    )
