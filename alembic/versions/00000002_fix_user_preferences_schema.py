"""Fix user_preferences schema mismatch

Revision ID: 00000002
Revises: 00000001
Create Date: 2025-09-15 14:45:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB


# revision identifiers, used by Alembic.
revision = '00000002'
down_revision = '00000001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Drop the existing user_preferences table with wrong schema
    op.drop_table('user_preferences')
    
    # Recreate user_preferences table with correct schema
    op.create_table('user_preferences',
        sa.Column('id', sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', sa.dialects.postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id'), unique=True, nullable=False),
        sa.Column('theme', sa.String(20), default='system', nullable=False),
        sa.Column('language', sa.String(10), default='en', nullable=False),
        sa.Column('currency', sa.String(3), default='USD', nullable=False),
        sa.Column('notification_settings', JSONB, default={
            'push_enabled': True,
            'email_enabled': True,
            'list_updates': True,
            'reminders': True,
            'social_updates': True
        }),
        sa.Column('privacy_settings', JSONB, default={
            'profile_visibility': 'friends',
            'show_online_status': True,
            'allow_friend_requests': True,
            'show_shared_lists': True
        }),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now())
    )


def downgrade() -> None:
    # Drop the corrected table
    op.drop_table('user_preferences')
    
    # Recreate the old incorrect schema (for rollback)
    op.create_table('user_preferences',
        sa.Column('id', sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', sa.dialects.postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id'), unique=True, nullable=False),
        sa.Column('language', sa.String(10), default='en', nullable=False),
        sa.Column('currency', sa.String(3), default='USD', nullable=False),
        sa.Column('notifications_enabled', sa.Boolean, default=True, nullable=False),
        sa.Column('email_notifications', sa.Boolean, default=True, nullable=False),
        sa.Column('push_notifications', sa.Boolean, default=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now())
    )
