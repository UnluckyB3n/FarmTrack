"""add_auth_provider_to_users

Revision ID: c1f93c2eb9e7
Revises: cb052218d78a
Create Date: 2025-11-18 22:56:52.707707

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = 'c1f93c2eb9e7'
down_revision = 'cb052218d78a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add auth_provider column to users table
    op.add_column('users', sa.Column('auth_provider', sa.String(), nullable=True))
    
    # Set default value for existing users
    op.execute("UPDATE users SET auth_provider = 'credentials' WHERE auth_provider IS NULL")


def downgrade() -> None:
    # Remove auth_provider column from users table
    op.drop_column('users', 'auth_provider')