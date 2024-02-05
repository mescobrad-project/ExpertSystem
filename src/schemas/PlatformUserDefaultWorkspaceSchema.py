from datetime import datetime
from pydantic import Field
from uuid import UUID, uuid4
from src.schemas._base import Base, FormBase


# Shared properties
class PlatformUserDefaultWorkspaceBase(FormBase):
    ws_id: int
    user_name: str
    status: str
    updated_on: datetime = None


# Properties to receive on obj creation
class PlatformUserDefaultWorkspaceCreate(PlatformUserDefaultWorkspaceBase):
    pass


# Properties to receive on obj update
class PlatformUserDefaultWorkspaceUpdate(PlatformUserDefaultWorkspaceBase):
    pass


# Properties shared by models stored in DB
class PlatformUserDefaultWorkspaceInDBBase(Base):
    usr_def_ws_id: int
    ws_id: int
    user_name: str = None
    status: str = None
    updated_on: datetime = None

    class Config:
        orm_mode = True


# Properties to return to client
class PlatformUserDefaultWorkspace(PlatformUserDefaultWorkspaceInDBBase):
    pass


# Properties stored in DB
class PlatformUserDefaultWorkspaceInDB(PlatformUserDefaultWorkspaceInDBBase):
    pass
