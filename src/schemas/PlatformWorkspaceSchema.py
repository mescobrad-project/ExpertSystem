from datetime import datetime
from src.schemas._base import Base, BaseModel


# Shared properties
class PlatformWorkspaceBase(BaseModel):
    ws_name: str
    ws_description: str
    ws_type: str
    ws_owner: str
    ws_status: str
    ws_role: str
    ws_created_on: datetime = None


# Properties to receive on obj creation
class PlatformWorkspaceCreate(PlatformWorkspaceBase):
    pass


# Properties to receive on obj update
class PlatformWorkspaceUpdate(PlatformWorkspaceBase):
    pass


# Properties shared by models stored in DB
class PlatformWorkspaceInDBBase(Base):
    ws_id: int
    ws_name: str = None
    ws_description: str = None
    ws_type: str = None
    ws_owner: str = None
    ws_status: str = None
    ws_role: str = None
    ws_created_on: datetime = None

    class Config:
        orm_mode = True


# Properties to return to client
class PlatformWorkspace(PlatformWorkspaceInDBBase):
    pass


# Properties stored in DB
class PlatformWorkspaceInDB(PlatformWorkspaceInDBBase):
    pass
