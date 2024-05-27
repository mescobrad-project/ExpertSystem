"""run models fix 2

Revision ID: e41dffdf820c
Revises: aca5d96e7443
Create Date: 2024-05-27 14:15:27.924946

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e41dffdf820c'
down_revision = 'aca5d96e7443'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    #op.drop_constraint('files_ws_id_fkey', 'files', type_='foreignkey')
    #op.create_foreign_key(None, 'files', 'mcb_workspaces', ['ws_id'], ['ws_id'], source_schema='public', referent_schema='public')
    #op.drop_constraint('mcb_user_default_workspace_ws_id_fkey', 'mcb_user_default_workspace', type_='foreignkey')
    #op.create_foreign_key(None, 'mcb_user_default_workspace', 'mcb_workspaces', ['ws_id'], ['ws_id'], source_schema='public', referent_schema='public')
    # op.drop_constraint('modules_category_id_fkey', 'modules', type_='foreignkey')
    # op.create_foreign_key(None, 'modules', 'module_categories', ['category_id'], ['id'], source_schema='public', referent_schema='public')
    op.add_column('new_workflow_actions', sa.Column('input', sa.String(), nullable=True))
    # op.drop_constraint('new_workflows_ws_id_fkey', 'new_workflows', type_='foreignkey')
    # op.create_foreign_key(None, 'new_workflows', 'mcb_workspaces', ['ws_id'], ['ws_id'], source_schema='public', referent_schema='public')
    # op.drop_constraint('runs_workflow_id_fkey', 'runs', type_='foreignkey')
    # op.drop_constraint('runs_ws_id_fkey', 'runs', type_='foreignkey')
    # op.create_foreign_key(None, 'runs', 'mcb_workspaces', ['ws_id'], ['ws_id'], source_schema='public', referent_schema='public')
    # op.create_foreign_key(None, 'runs', 'workflows', ['workflow_id'], ['id'], source_schema='public', referent_schema='public')
    # op.drop_constraint('variables_features_variable_id_fkey', 'variables_features', type_='foreignkey')
    # op.drop_constraint('variables_features_feature_id_fkey', 'variables_features', type_='foreignkey')
    # op.create_foreign_key(None, 'variables_features', 'variables', ['variable_id'], ['id'], source_schema='public', referent_schema='public')
    # op.create_foreign_key(None, 'variables_features', 'features', ['feature_id'], ['id'], source_schema='public', referent_schema='public')
    # op.drop_constraint('workflows_category_id_fkey', 'workflows', type_='foreignkey')
    # op.drop_constraint('workflows_ws_id_fkey', 'workflows', type_='foreignkey')
    # op.create_foreign_key(None, 'workflows', 'workflow_categories', ['category_id'], ['id'], source_schema='public', referent_schema='public')
    # op.create_foreign_key(None, 'workflows', 'mcb_workspaces', ['ws_id'], ['ws_id'], source_schema='public', referent_schema='public')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'workflows', schema='public', type_='foreignkey')
    op.drop_constraint(None, 'workflows', schema='public', type_='foreignkey')
    op.create_foreign_key('workflows_ws_id_fkey', 'workflows', 'mcb_workspaces', ['ws_id'], ['ws_id'])
    op.create_foreign_key('workflows_category_id_fkey', 'workflows', 'workflow_categories', ['category_id'], ['id'])
    op.drop_constraint(None, 'variables_features', schema='public', type_='foreignkey')
    op.drop_constraint(None, 'variables_features', schema='public', type_='foreignkey')
    op.create_foreign_key('variables_features_feature_id_fkey', 'variables_features', 'features', ['feature_id'], ['id'])
    op.create_foreign_key('variables_features_variable_id_fkey', 'variables_features', 'variables', ['variable_id'], ['id'])
    op.drop_constraint(None, 'runs', schema='public', type_='foreignkey')
    op.drop_constraint(None, 'runs', schema='public', type_='foreignkey')
    op.create_foreign_key('runs_ws_id_fkey', 'runs', 'mcb_workspaces', ['ws_id'], ['ws_id'])
    op.create_foreign_key('runs_workflow_id_fkey', 'runs', 'workflows', ['workflow_id'], ['id'])
    op.drop_constraint(None, 'new_workflows', schema='public', type_='foreignkey')
    op.create_foreign_key('new_workflows_ws_id_fkey', 'new_workflows', 'mcb_workspaces', ['ws_id'], ['ws_id'])
    op.drop_column('new_workflow_actions', 'input')
    op.drop_constraint(None, 'modules', schema='public', type_='foreignkey')
    op.create_foreign_key('modules_category_id_fkey', 'modules', 'module_categories', ['category_id'], ['id'])
    op.drop_constraint(None, 'mcb_user_default_workspace', schema='public', type_='foreignkey')
    op.create_foreign_key('mcb_user_default_workspace_ws_id_fkey', 'mcb_user_default_workspace', 'mcb_workspaces', ['ws_id'], ['ws_id'])
    op.drop_constraint(None, 'files', schema='public', type_='foreignkey')
    op.create_foreign_key('files_ws_id_fkey', 'files', 'mcb_workspaces', ['ws_id'], ['ws_id'])
    # ### end Alembic commands ###
