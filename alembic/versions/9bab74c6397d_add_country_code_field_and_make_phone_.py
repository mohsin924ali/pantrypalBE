"""Add country_code field and make phone_email mandatory

Revision ID: 9bab74c6397d
Revises: 
Create Date: 2025-08-25 19:39:16.812477

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9bab74c6397d'
down_revision = '00000000'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # This migration is now a no-op since the initial migration (00000000)
    # already creates the users table with the correct schema including:
    # - country_code field as non-nullable
    # - email and phone as non-nullable
    # - unique_phone_per_country constraint
    pass


def downgrade() -> None:
    # This migration is now a no-op
    pass
