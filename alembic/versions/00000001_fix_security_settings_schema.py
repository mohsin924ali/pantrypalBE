"""Fix security_settings schema mismatch

Revision ID: 00000001
Revises: 9bab74c6397d
Create Date: 2025-09-15 14:30:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '00000001'
down_revision = '9bab74c6397d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Drop the existing security_settings table with wrong schema
    op.drop_table('security_settings')
    
    # Recreate security_settings table with correct schema
    op.create_table('security_settings',
        sa.Column('id', sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', sa.dialects.postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id'), unique=True, nullable=False),
        sa.Column('biometric_enabled', sa.Boolean, default=False, nullable=False),
        sa.Column('login_alerts', sa.Boolean, default=True, nullable=False),
        sa.Column('session_timeout', sa.Integer, default=1800, nullable=False),
        sa.Column('max_sessions', sa.Integer, default=5, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now())
    )
    
    # Drop the existing biometric_keys table with wrong foreign key
    op.drop_table('biometric_keys')
    
    # Recreate biometric_keys table with correct schema
    op.create_table('biometric_keys',
        sa.Column('id', sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('security_settings_id', sa.dialects.postgresql.UUID(as_uuid=True), sa.ForeignKey('security_settings.id'), nullable=False),
        sa.Column('device_id', sa.String(255), nullable=False),
        sa.Column('public_key', sa.Text, nullable=False),
        sa.Column('key_type', sa.String(50), default='biometric', nullable=False),
        sa.Column('is_active', sa.Boolean, default=True, nullable=False),
        sa.Column('last_used_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now())
    )


def downgrade() -> None:
    # Drop the corrected tables
    op.drop_table('biometric_keys')
    op.drop_table('security_settings')
    
    # Recreate the old incorrect schema (if needed for rollback)
    op.create_table('security_settings',
        sa.Column('id', sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', sa.dialects.postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id'), unique=True, nullable=False),
        sa.Column('biometric_enabled', sa.Boolean, default=False, nullable=False),
        sa.Column('session_timeout_minutes', sa.Integer, default=30, nullable=False),
        sa.Column('auto_lock_enabled', sa.Boolean, default=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now())
    )
    
    op.create_table('biometric_keys',
        sa.Column('id', sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', sa.dialects.postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('device_id', sa.String(255), nullable=False),
        sa.Column('key_hash', sa.String(255), nullable=False),
        sa.Column('key_type', sa.String(50), nullable=False),
        sa.Column('is_active', sa.Boolean, default=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('last_used_at', sa.DateTime(timezone=True), nullable=True)
    )
