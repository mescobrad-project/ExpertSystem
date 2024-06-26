"""NewWorkflows

Revision ID: 51e3d799b2fa
Revises: cb1d53933ec6
Create Date: 2024-05-15 15:12:58.899665

"""
from alembic import op
import sqlalchemy as sa
import src.models._base


# revision identifiers, used by Alembic.
revision = '51e3d799b2fa'
down_revision = 'cb1d53933ec6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('new_workflow_action_conditionals',
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('workflow_action_id', sa.String(), nullable=True),
    sa.Column('type', sa.String(), nullable=True),
    sa.Column('order', sa.Integer(), nullable=True),
    sa.Column('weight', sa.Integer(), nullable=True),
    sa.Column('variable', sa.String(), nullable=True),
    sa.Column('value', sa.String(), nullable=True),
    sa.Column('metadata_value', sa.String(), nullable=True),
    sa.Column('ws_id', sa.Integer(), nullable=True),
    sa.Column('id', src.models._base.GUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    schema='public'
    )
    op.create_index(op.f('ix_public_new_workflow_action_conditionals_name'), 'new_workflow_action_conditionals', ['name'], unique=False, schema='public')
    op.create_index(op.f('ix_public_new_workflow_action_conditionals_order'), 'new_workflow_action_conditionals', ['order'], unique=False, schema='public')
    op.create_index(op.f('ix_public_new_workflow_action_conditionals_type'), 'new_workflow_action_conditionals', ['type'], unique=False, schema='public')
    op.create_index(op.f('ix_public_new_workflow_action_conditionals_workflow_action_id'), 'new_workflow_action_conditionals', ['workflow_action_id'], unique=False, schema='public')
    op.create_index(op.f('ix_public_new_workflow_action_conditionals_ws_id'), 'new_workflow_action_conditionals', ['ws_id'], unique=False, schema='public')
    op.create_table('new_workflow_actions',
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('workflow_step_id', sa.String(), nullable=True),
    sa.Column('type', sa.String(), nullable=True),
    sa.Column('order', sa.Integer(), nullable=True),
    sa.Column('is_conditional', sa.Boolean(), nullable=True),
    sa.Column('action', sa.String(), nullable=False),
    sa.Column('weight_to_true', sa.Integer(), nullable=True),
    sa.Column('ws_id', sa.Integer(), nullable=True),
    sa.Column('id', src.models._base.GUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    schema='public'
    )
    op.create_index(op.f('ix_public_new_workflow_actions_name'), 'new_workflow_actions', ['name'], unique=False, schema='public')
    op.create_index(op.f('ix_public_new_workflow_actions_order'), 'new_workflow_actions', ['order'], unique=False, schema='public')
    op.create_index(op.f('ix_public_new_workflow_actions_type'), 'new_workflow_actions', ['type'], unique=False, schema='public')
    op.create_index(op.f('ix_public_new_workflow_actions_workflow_step_id'), 'new_workflow_actions', ['workflow_step_id'], unique=False, schema='public')
    op.create_index(op.f('ix_public_new_workflow_actions_ws_id'), 'new_workflow_actions', ['ws_id'], unique=False, schema='public')
    op.create_table('new_workflow_steps',
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('workflow_id', sa.String(), nullable=True),
    sa.Column('type', sa.String(), nullable=True),
    sa.Column('order', sa.Integer(), nullable=True),
    sa.Column('ws_id', sa.Integer(), nullable=True),
    sa.Column('id', src.models._base.GUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    schema='public'
    )
    op.create_index(op.f('ix_public_new_workflow_steps_name'), 'new_workflow_steps', ['name'], unique=False, schema='public')
    op.create_index(op.f('ix_public_new_workflow_steps_order'), 'new_workflow_steps', ['order'], unique=False, schema='public')
    op.create_index(op.f('ix_public_new_workflow_steps_type'), 'new_workflow_steps', ['type'], unique=False, schema='public')
    op.create_index(op.f('ix_public_new_workflow_steps_workflow_id'), 'new_workflow_steps', ['workflow_id'], unique=False, schema='public')
    op.create_index(op.f('ix_public_new_workflow_steps_ws_id'), 'new_workflow_steps', ['ws_id'], unique=False, schema='public')
    op.create_table('new_workflows',
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('category_id', sa.String(), nullable=True),
    sa.Column('is_template', sa.Boolean(), nullable=True),
    sa.Column('is_part_of_other', sa.Boolean(), nullable=True),
    sa.Column('json_representation', sa.JSON(), nullable=True),
    sa.Column('id', src.models._base.GUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('ws_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['ws_id'], ['public.mcb_workspaces.ws_id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='public'
    )
    op.create_index(op.f('ix_public_new_workflows_category_id'), 'new_workflows', ['category_id'], unique=False, schema='public')
    op.create_index(op.f('ix_public_new_workflows_name'), 'new_workflows', ['name'], unique=False, schema='public')
    op.create_index(op.f('ix_public_new_workflows_ws_id'), 'new_workflows', ['ws_id'], unique=False, schema='public')
    op.drop_constraint('files_ws_id_fkey', 'files', type_='foreignkey')
    op.create_foreign_key(None, 'files', 'mcb_workspaces', ['ws_id'], ['ws_id'], source_schema='public', referent_schema='public')
    op.drop_constraint('mcb_user_default_workspace_ws_id_fkey', 'mcb_user_default_workspace', type_='foreignkey')
    op.create_foreign_key(None, 'mcb_user_default_workspace', 'mcb_workspaces', ['ws_id'], ['ws_id'], source_schema='public', referent_schema='public')
    op.drop_constraint('modules_category_id_fkey', 'modules', type_='foreignkey')
    op.create_foreign_key(None, 'modules', 'module_categories', ['category_id'], ['id'], source_schema='public', referent_schema='public')
    op.drop_constraint('runs_workflow_id_fkey', 'runs', type_='foreignkey')
    op.drop_constraint('runs_ws_id_fkey', 'runs', type_='foreignkey')
    op.create_foreign_key(None, 'runs', 'workflows', ['workflow_id'], ['id'], source_schema='public', referent_schema='public')
    op.create_foreign_key(None, 'runs', 'mcb_workspaces', ['ws_id'], ['ws_id'], source_schema='public', referent_schema='public')
    op.drop_constraint('variables_features_variable_id_fkey', 'variables_features', type_='foreignkey')
    op.drop_constraint('variables_features_feature_id_fkey', 'variables_features', type_='foreignkey')
    op.create_foreign_key(None, 'variables_features', 'variables', ['variable_id'], ['id'], source_schema='public', referent_schema='public')
    op.create_foreign_key(None, 'variables_features', 'features', ['feature_id'], ['id'], source_schema='public', referent_schema='public')
    op.drop_constraint('workflows_ws_id_fkey', 'workflows', type_='foreignkey')
    op.drop_constraint('workflows_category_id_fkey', 'workflows', type_='foreignkey')
    op.create_foreign_key(None, 'workflows', 'mcb_workspaces', ['ws_id'], ['ws_id'], source_schema='public', referent_schema='public')
    op.create_foreign_key(None, 'workflows', 'workflow_categories', ['category_id'], ['id'], source_schema='public', referent_schema='public')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'workflows', schema='public', type_='foreignkey')
    op.drop_constraint(None, 'workflows', schema='public', type_='foreignkey')
    op.create_foreign_key('workflows_category_id_fkey', 'workflows', 'workflow_categories', ['category_id'], ['id'])
    op.create_foreign_key('workflows_ws_id_fkey', 'workflows', 'mcb_workspaces', ['ws_id'], ['ws_id'])
    op.drop_constraint(None, 'variables_features', schema='public', type_='foreignkey')
    op.drop_constraint(None, 'variables_features', schema='public', type_='foreignkey')
    op.create_foreign_key('variables_features_feature_id_fkey', 'variables_features', 'features', ['feature_id'], ['id'])
    op.create_foreign_key('variables_features_variable_id_fkey', 'variables_features', 'variables', ['variable_id'], ['id'])
    op.drop_constraint(None, 'runs', schema='public', type_='foreignkey')
    op.drop_constraint(None, 'runs', schema='public', type_='foreignkey')
    op.create_foreign_key('runs_ws_id_fkey', 'runs', 'mcb_workspaces', ['ws_id'], ['ws_id'])
    op.create_foreign_key('runs_workflow_id_fkey', 'runs', 'workflows', ['workflow_id'], ['id'])
    op.drop_constraint(None, 'modules', schema='public', type_='foreignkey')
    op.create_foreign_key('modules_category_id_fkey', 'modules', 'module_categories', ['category_id'], ['id'])
    op.drop_constraint(None, 'mcb_user_default_workspace', schema='public', type_='foreignkey')
    op.create_foreign_key('mcb_user_default_workspace_ws_id_fkey', 'mcb_user_default_workspace', 'mcb_workspaces', ['ws_id'], ['ws_id'])
    op.drop_constraint(None, 'files', schema='public', type_='foreignkey')
    op.create_foreign_key('files_ws_id_fkey', 'files', 'mcb_workspaces', ['ws_id'], ['ws_id'])
    op.drop_index(op.f('ix_public_new_workflows_ws_id'), table_name='new_workflows', schema='public')
    op.drop_index(op.f('ix_public_new_workflows_name'), table_name='new_workflows', schema='public')
    op.drop_index(op.f('ix_public_new_workflows_category_id'), table_name='new_workflows', schema='public')
    op.drop_table('new_workflows', schema='public')
    op.drop_index(op.f('ix_public_new_workflow_steps_ws_id'), table_name='new_workflow_steps', schema='public')
    op.drop_index(op.f('ix_public_new_workflow_steps_workflow_id'), table_name='new_workflow_steps', schema='public')
    op.drop_index(op.f('ix_public_new_workflow_steps_type'), table_name='new_workflow_steps', schema='public')
    op.drop_index(op.f('ix_public_new_workflow_steps_order'), table_name='new_workflow_steps', schema='public')
    op.drop_index(op.f('ix_public_new_workflow_steps_name'), table_name='new_workflow_steps', schema='public')
    op.drop_table('new_workflow_steps', schema='public')
    op.drop_index(op.f('ix_public_new_workflow_actions_ws_id'), table_name='new_workflow_actions', schema='public')
    op.drop_index(op.f('ix_public_new_workflow_actions_workflow_step_id'), table_name='new_workflow_actions', schema='public')
    op.drop_index(op.f('ix_public_new_workflow_actions_type'), table_name='new_workflow_actions', schema='public')
    op.drop_index(op.f('ix_public_new_workflow_actions_order'), table_name='new_workflow_actions', schema='public')
    op.drop_index(op.f('ix_public_new_workflow_actions_name'), table_name='new_workflow_actions', schema='public')
    op.drop_table('new_workflow_actions', schema='public')
    op.drop_index(op.f('ix_public_new_workflow_action_conditionals_ws_id'), table_name='new_workflow_action_conditionals', schema='public')
    op.drop_index(op.f('ix_public_new_workflow_action_conditionals_workflow_action_id'), table_name='new_workflow_action_conditionals', schema='public')
    op.drop_index(op.f('ix_public_new_workflow_action_conditionals_type'), table_name='new_workflow_action_conditionals', schema='public')
    op.drop_index(op.f('ix_public_new_workflow_action_conditionals_order'), table_name='new_workflow_action_conditionals', schema='public')
    op.drop_index(op.f('ix_public_new_workflow_action_conditionals_name'), table_name='new_workflow_action_conditionals', schema='public')
    op.drop_table('new_workflow_action_conditionals', schema='public')
    # ### end Alembic commands ###
