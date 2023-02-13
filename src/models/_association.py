from sqlalchemy.orm import Mapped, relationship
from .ModuleModel import BaseModuleModel
from .ModuleCategoryModel import BaseModuleCategoryModel
from .UserModel import BaseUserModel
from .FileModel import BaseFileModel
from .WorkflowCategoryModel import BaseWorkflowCategoryModel
from .WorkflowModel import BaseWorkflowModel
from .RunModel import BaseRunModel


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
