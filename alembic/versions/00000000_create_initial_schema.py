"""Create initial database schema

Revision ID: 00000000
Revises: 
Create Date: 2025-09-15 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB


# revision identifiers, used by Alembic.
revision = '00000000'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create users table
    op.create_table('users',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('email', sa.String(255), unique=True, index=True, nullable=False),
        sa.Column('phone', sa.String(15), nullable=False),
        sa.Column('country_code', sa.String(4), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('avatar_url', sa.Text, nullable=True),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('is_active', sa.Boolean, default=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint('phone', 'country_code', name='unique_phone_per_country')
    )

    # Create user_preferences table
    op.create_table('user_preferences',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id'), unique=True, nullable=False),
        sa.Column('language', sa.String(10), default='en', nullable=False),
        sa.Column('currency', sa.String(3), default='USD', nullable=False),
        sa.Column('notifications_enabled', sa.Boolean, default=True, nullable=False),
        sa.Column('email_notifications', sa.Boolean, default=True, nullable=False),
        sa.Column('push_notifications', sa.Boolean, default=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now())
    )

    # Create security_settings table
    op.create_table('security_settings',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id'), unique=True, nullable=False),
        sa.Column('biometric_enabled', sa.Boolean, default=False, nullable=False),
        sa.Column('login_alerts', sa.Boolean, default=True, nullable=False),
        sa.Column('session_timeout', sa.Integer, default=1800, nullable=False),
        sa.Column('max_sessions', sa.Integer, default=5, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now())
    )

    # Create biometric_keys table
    op.create_table('biometric_keys',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('security_settings_id', UUID(as_uuid=True), sa.ForeignKey('security_settings.id'), nullable=False),
        sa.Column('device_id', sa.String(255), nullable=False),
        sa.Column('public_key', sa.Text, nullable=False),
        sa.Column('key_type', sa.String(50), default='biometric', nullable=False),
        sa.Column('is_active', sa.Boolean, default=True, nullable=False),
        sa.Column('last_used_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now())
    )

    # Create item_categories table
    op.create_table('item_categories',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(100), unique=True, nullable=False, index=True),
        sa.Column('color', sa.String(7), nullable=False),
        sa.Column('icon', sa.String(50), nullable=True),
        sa.Column('is_system', sa.Boolean, default=False, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now())
    )

    # Create shopping_lists table
    op.create_table('shopping_lists',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('owner_id', UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('status', sa.String(20), default='active', nullable=False),
        sa.Column('budget_amount', sa.Numeric(10, 2), nullable=True),
        sa.Column('budget_currency', sa.String(3), default='USD', nullable=True),
        sa.Column('meta_data', JSONB, default={}),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now())
    )

    # Create shopping_items table
    op.create_table('shopping_items',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('shopping_list_id', UUID(as_uuid=True), sa.ForeignKey('shopping_lists.id'), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('category_id', UUID(as_uuid=True), sa.ForeignKey('item_categories.id'), nullable=True),
        sa.Column('quantity', sa.Numeric(10, 3), default=1, nullable=False),
        sa.Column('unit', sa.String(50), default='pcs', nullable=False),
        sa.Column('estimated_price', sa.Numeric(10, 2), nullable=True),
        sa.Column('actual_price', sa.Numeric(10, 2), nullable=True),
        sa.Column('currency', sa.String(3), default='USD', nullable=True),
        sa.Column('notes', sa.Text, nullable=True),
        sa.Column('is_completed', sa.Boolean, default=False, nullable=False),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('assigned_user_id', UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('barcode', sa.String(50), nullable=True),
        sa.Column('image_url', sa.Text, nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now())
    )

    # Create list_collaborators table
    op.create_table('list_collaborators',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('shopping_list_id', UUID(as_uuid=True), sa.ForeignKey('shopping_lists.id'), nullable=False),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('permission_level', sa.String(20), default='editor', nullable=False),
        sa.Column('invited_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('joined_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('status', sa.String(20), default='pending', nullable=False),
        sa.UniqueConstraint('shopping_list_id', 'user_id', name='unique_list_collaborator')
    )

    # Create friendships table
    op.create_table('friendships',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('user1_id', UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('user2_id', UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('status', sa.String(20), default='active', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint('user1_id', 'user2_id', name='unique_friendship'),
        sa.CheckConstraint('user1_id != user2_id', name='no_self_friendship')
    )

    # Create friend_requests table
    op.create_table('friend_requests',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('from_user_id', UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('to_user_id', UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('message', sa.Text, nullable=True),
        sa.Column('status', sa.String(20), default='pending', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('responded_at', sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint('from_user_id', 'to_user_id', name='unique_friend_request'),
        sa.CheckConstraint('from_user_id != to_user_id', name='no_self_friend_request')
    )

    # Create pantry_items table
    op.create_table('pantry_items',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('category_id', UUID(as_uuid=True), sa.ForeignKey('item_categories.id'), nullable=True),
        sa.Column('quantity', sa.Numeric(10, 3), default=1, nullable=False),
        sa.Column('unit', sa.String(50), default='pcs', nullable=False),
        sa.Column('location', sa.String(100), nullable=True),
        sa.Column('expiration_date', sa.Date, nullable=True),
        sa.Column('low_stock_threshold', sa.Numeric(10, 3), default=1, nullable=False),
        sa.Column('barcode', sa.String(50), nullable=True),
        sa.Column('image_url', sa.Text, nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now())
    )

    # Create activity_logs table
    op.create_table('activity_logs',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('entity_type', sa.String(50), nullable=False),
        sa.Column('entity_id', UUID(as_uuid=True), nullable=True),
        sa.Column('action', sa.String(50), nullable=False),
        sa.Column('meta_data', JSONB, default={}),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now())
    )


def downgrade() -> None:
    # Drop tables in reverse order of creation
    op.drop_table('activity_logs')
    op.drop_table('pantry_items')
    op.drop_table('friend_requests')
    op.drop_table('friendships')
    op.drop_table('list_collaborators')
    op.drop_table('shopping_items')
    op.drop_table('shopping_lists')
    op.drop_table('item_categories')
    op.drop_table('biometric_keys')
    op.drop_table('security_settings')
    op.drop_table('user_preferences')
    op.drop_table('users')
