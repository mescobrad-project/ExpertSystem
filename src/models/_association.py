from typing import List
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import Mapped, relationship, mapped_column
from src.config import DB_SCHEMA
from src.models.NewRunActionModel import BaseNewRunActionModel
from src.models.NewRunModel import BaseNewRunModel
from ._base import Base, GUID
from .ModuleModel import BaseModuleModel
from .ModuleCategoryModel import BaseModuleCategoryModel
from .PlatformUserDefaultWorkspaceModel import BasePlatformUserDefaultWorkspaceModel
from .PlatformWorkspaceModel import BasePlatformWorkspaceModel
from .FeatureModel import BaseFeatureModel
from .VariableModel import BaseVariableModel
from .UserModel import BaseUserModel
from .FileModel import BaseFileModel
from .WorkflowCategoryModel import BaseWorkflowCategoryModel
from .WorkflowModel import BaseWorkflowModel
from .RunModel import BaseRunModel
from .NewWorkflowModel import BaseNewWorkflowModel
from .NewWorkflowStepModel import BaseNewWorkflowStepModel
from .NewWorkflowActionModel import BaseNewWorkflowActionModel
from .NewWorkflowActionConditionalModel import BaseNewWorkflowActionConditionalModel

Base.metadata.schema = DB_SCHEMA

variables_features = Table(
    "variables_features",
    Base.metadata,
    Column("variable_id", ForeignKey(f"{DB_SCHEMA}.variables.id"), primary_key=True),
    Column("feature_id", ForeignKey(f"{DB_SCHEMA}.features.id"), primary_key=True),
)


class PlatformWorkspaceModel(BasePlatformWorkspaceModel):
    user_workspaces: Mapped[List["PlatformUserDefaultWorkspaceModel"]] = relationship(
        back_populates="workspace"
    )


class PlatformUserDefaultWorkspaceModel(BasePlatformUserDefaultWorkspaceModel):
    workspace: Mapped["PlatformWorkspaceModel"] = relationship(
        back_populates="user_workspaces"
    )
    ws_id: Mapped[int] = mapped_column(
        ForeignKey(
            f"{BasePlatformUserDefaultWorkspaceModel.__table_args__['schema']}.{PlatformWorkspaceModel.__tablename__}.ws_id"
        ),
        index=True,
        nullable=True,
    )


class FeatureModel(BaseFeatureModel):
    variables: Mapped[list["VariableModel"]] = relationship(
        secondary=variables_features, back_populates="features", cascade="all"
    )


class VariableModel(BaseVariableModel):
    features: Mapped[list["FeatureModel"]] = relationship(
        secondary=variables_features, back_populates="variables", cascade="all"
    )


class UserModel(BaseUserModel):
    pass


class FileModel(BaseFileModel):
    ws_id: Mapped[int] = mapped_column(
        ForeignKey(
            f"{BasePlatformUserDefaultWorkspaceModel.__table_args__['schema']}.{PlatformWorkspaceModel.__tablename__}.ws_id"
        ),
        index=True,
        nullable=True,
    )


class ModuleCategoryModel(BaseModuleCategoryModel):
    modules: Mapped["ModuleModel"] = relationship(back_populates="category")


class ModuleModel(BaseModuleModel):
    category: Mapped["ModuleCategoryModel"] = relationship(back_populates="modules")


class WorkflowCategoryModel(BaseWorkflowCategoryModel):
    workflows: Mapped["WorkflowModel"] = relationship(back_populates="category")


class WorkflowModel(BaseWorkflowModel):
    runs: Mapped["RunModel"] = relationship(back_populates="workflow")
    category: Mapped["WorkflowCategoryModel"] = relationship(back_populates="workflows")
    ws_id: Mapped[int] = mapped_column(
        ForeignKey(
            f"{BasePlatformUserDefaultWorkspaceModel.__table_args__['schema']}.{PlatformWorkspaceModel.__tablename__}.ws_id"
        ),
        index=True,
        nullable=True,
    )


class RunModel(BaseRunModel):
    workflow: Mapped["WorkflowModel"] = relationship(back_populates="runs")
    ws_id: Mapped[int] = mapped_column(
        ForeignKey(
            f"{BasePlatformUserDefaultWorkspaceModel.__table_args__['schema']}.{PlatformWorkspaceModel.__tablename__}.ws_id"
        ),
        index=True,
        nullable=True,
    )


class NewWorkflowModel(BaseNewWorkflowModel):
    ws_id: Mapped[int] = mapped_column(
        ForeignKey(
            f"{BasePlatformUserDefaultWorkspaceModel.__table_args__['schema']}.{PlatformWorkspaceModel.__tablename__}.ws_id"
        ),
        index=True,
        nullable=True,
    )


class NewWorkflowStepModel(BaseNewWorkflowStepModel):
    pass


class NewWorkflowActionModel(BaseNewWorkflowActionModel):
    pass


class NewWorkflowActionConditionalModel(BaseNewWorkflowActionConditionalModel):
    pass

class NewRunModel(BaseNewRunModel):
    pass

class NewRunActionModel(BaseNewRunActionModel):
    pass
