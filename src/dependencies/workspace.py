from fastapi import Depends, Header
from sqlalchemy.orm import Session
from src.controllers.PlatformUserDefaultWorkspaceController import (
    PlatformUserDefaultWorkspaceController,
)
from src.controllers.PlatformWorkspaceController import PlatformWorkspaceController
from src.database import get_db
from src.errors.ApiRequestException import (
    ForbiddenException,
    UnauthorizedException,
    NotFoundException,
)
from src.schemas.PlatformWorkspaceSchema import PlatformWorkspace
from .authentication import get_user


def _prepare_wsid(db, workspace: PlatformWorkspace, x_es_token, raise_a_raise=True):
    user, token, _ = get_user(x_es_token, db)

    if not token:
        raise UnauthorizedException(message="Invalid Access Token")

    try:
        user_name = user.info["preferred_username"]
        user_workspace = PlatformUserDefaultWorkspaceController.read_by_ws_id(
            db, workspace.ws_id, {"user_name": user_name}
        )
    except:
        if raise_a_raise:
            raise ForbiddenException(
                message=f"User does not have access to workspace {workspace.ws_name}"
            )

    return user_workspace.ws_id


async def validate_workspace(
    x_es_token: str = Header(), x_es_wsid: str = Header(), db: Session = Depends(get_db)
):
    if x_es_wsid == None or x_es_wsid == "null":
        raise UnauthorizedException(message="Invalid Workspace ID")

    try:
        workspace = PlatformWorkspaceController.read(db, x_es_wsid)
    except:
        raise NotFoundException(message="Invalid Workspace")

    ws_id = _prepare_wsid(db, workspace, x_es_token)

    if not ws_id:
        raise UnauthorizedException(message="Invalid Workspace ID")

    return ws_id


# Done
#     Pass workspace id through iframe
#     Start investigation for Recommendation Engine

# To do
#     Sync DA module list with ones in ES
#     Add Access Control logic in ES for DataLake interactions
#     Allow users to get their created datasets filtered by Workspace
#     Change Category-WF and Variable-WF mappings in ES
#     Migration of workflows

# Backlog
#     BPM Metadata generation
#     Standardise DA modules output with KB (first steps)


# Realm Roles
#     metadata_admin
#     upload-data
#     view-*

# Clients
#     the same as above

# Minio relies in keycloak groups. That will be changed with the wsid inside the data
# Note that might be a problem in where the datasets are stored
