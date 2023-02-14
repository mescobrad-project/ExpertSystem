from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import Mapped, relationship
from src.config import DB_SCHEMA
from ._base import Base
from .ModuleModel import BaseModuleModel
from .ModuleCategoryModel import BaseModuleCategoryModel
from .FeatureModel import BaseFeatureModel
from .VariableModel import BaseVariableModel
from .UserModel import BaseUserModel
from .FileModel import BaseFileModel
from .WorkflowCategoryModel import BaseWorkflowCategoryModel
from .WorkflowModel import BaseWorkflowModel
from .RunModel import BaseRunModel

Base.metadata.schema = DB_SCHEMA

variables_features = Table(
    "variables_features",
    Base.metadata,
    Column("variable_id", ForeignKey(f"{DB_SCHEMA}.variables.id"), primary_key=True),
    Column("feature_id", ForeignKey(f"{DB_SCHEMA}.features.id"), primary_key=True),
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
    files: Mapped[list["FileModel"]] = relationship(back_populates="user")


class FileModel(BaseFileModel):
    user: Mapped["UserModel"] = relationship(back_populates="files")


class ModuleCategoryModel(BaseModuleCategoryModel):
    modules: Mapped["ModuleModel"] = relationship(back_populates="category")


class ModuleModel(BaseModuleModel):
    category: Mapped["ModuleCategoryModel"] = relationship(back_populates="modules")


class WorkflowCategoryModel(BaseWorkflowCategoryModel):
    workflows: Mapped["WorkflowModel"] = relationship(back_populates="category")


class WorkflowModel(BaseWorkflowModel):
    runs: Mapped["RunModel"] = relationship(back_populates="workflow")
    category: Mapped["WorkflowCategoryModel"] = relationship(back_populates="workflows")


class RunModel(BaseRunModel):
    workflow: Mapped["WorkflowModel"] = relationship(back_populates="runs")
