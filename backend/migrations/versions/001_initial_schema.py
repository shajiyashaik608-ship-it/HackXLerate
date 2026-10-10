"""Initial database schema for Health Saathi

Revision ID: 001_initial_schema
Revises: None
Create Date: 2026-10-10 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = '001_initial_schema'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. users
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('full_name', sa.String(length=150), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='1'),
        sa.Column('is_verified', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('consent_given', sa.Boolean(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)

    # 2. health_profiles
    op.create_table(
        'health_profiles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('age', sa.Integer(), nullable=True),
        sa.Column('diet_type', sa.String(length=50), nullable=False, server_default='veg'),
        sa.Column('baseline_cycle_length', sa.Integer(), nullable=True),
        sa.Column('period_duration', sa.Integer(), nullable=True),
        sa.Column('wellness_goals', sa.Text(), nullable=True),
        sa.Column('allergies', sa.Text(), nullable=True),
        sa.Column('preferred_language', sa.String(length=10), nullable=False, server_default='en'),
        sa.Column('timezone', sa.String(length=50), nullable=False, server_default='Asia/Kolkata'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id')
    )

    # 3. medical_documents
    op.create_table(
        'medical_documents',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('file_name', sa.String(length=255), nullable=False),
        sa.Column('file_type', sa.String(length=50), nullable=False),
        sa.Column('file_path', sa.String(length=500), nullable=False),
        sa.Column('category', sa.String(length=100), nullable=False, server_default='lab_report'),
        sa.Column('processing_status', sa.String(length=50), nullable=False, server_default='uploaded'),
        sa.Column('ocr_raw_text', sa.Text(), nullable=True),
        sa.Column('doctor_notes', sa.Text(), nullable=True),
        sa.Column('upload_date', sa.Date(), nullable=False),
        sa.Column('error_message', sa.String(length=500), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # 4. biomarkers
    op.create_table(
        'biomarkers',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('document_id', sa.Integer(), nullable=True),
        sa.Column('test_name', sa.String(length=150), nullable=False),
        sa.Column('observed_value', sa.String(length=100), nullable=False),
        sa.Column('numeric_value', sa.Float(), nullable=True),
        sa.Column('unit', sa.String(length=50), nullable=False),
        sa.Column('reference_range_lower', sa.Float(), nullable=True),
        sa.Column('reference_range_upper', sa.Float(), nullable=True),
        sa.Column('reference_range_text', sa.String(length=150), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='needs_review'),
        sa.Column('test_date', sa.Date(), nullable=True),
        sa.Column('extraction_confidence', sa.Float(), nullable=False, server_default='0.8'),
        sa.Column('source_page', sa.Integer(), nullable=True),
        sa.Column('is_user_corrected', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('plain_explanation', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['document_id'], ['medical_documents.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # 5. cycle_records
    op.create_table(
        'cycle_records',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('start_date', sa.Date(), nullable=False),
        sa.Column('end_date', sa.Date(), nullable=True),
        sa.Column('duration_days', sa.Integer(), nullable=True),
        sa.Column('flow_intensity', sa.String(length=50), nullable=False, server_default='medium'),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # 6. symptom_records
    op.create_table(
        'symptom_records',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('recorded_date', sa.Date(), nullable=False),
        sa.Column('symptom_type', sa.String(length=100), nullable=False),
        sa.Column('severity', sa.String(length=50), nullable=False, server_default='mild'),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # 7. meal_items
    op.create_table(
        'meal_items',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('category', sa.String(length=50), nullable=False),
        sa.Column('diet_type', sa.String(length=50), nullable=False, server_default='veg'),
        sa.Column('is_budget_friendly', sa.Boolean(), nullable=False, server_default='1'),
        sa.Column('serving_size', sa.String(length=100), nullable=False, server_default='1 serving'),
        sa.Column('approx_calories', sa.Integer(), nullable=True),
        sa.Column('protein_grams', sa.Float(), nullable=True),
        sa.Column('fibre_grams', sa.Float(), nullable=True),
        sa.Column('ingredients', sa.Text(), nullable=True),
        sa.Column('nutrition_source', sa.String(length=200), nullable=False),
        sa.Column('pcos_benefits', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # 8. meal_plans & meal_plan_items
    op.create_table(
        'meal_plans',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('plan_date', sa.Date(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'meal_plan_items',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('meal_plan_id', sa.Integer(), nullable=False),
        sa.Column('meal_item_id', sa.Integer(), nullable=False),
        sa.Column('meal_slot', sa.String(length=50), nullable=False, server_default='breakfast'),
        sa.Column('servings', sa.Float(), nullable=False, server_default='1.0'),
        sa.ForeignKeyConstraint(['meal_item_id'], ['meal_items.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['meal_plan_id'], ['meal_plans.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # 9. care_reminders & reminder_completions
    op.create_table(
        'care_reminders',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('category', sa.String(length=100), nullable=False, server_default='medication'),
        sa.Column('scheduled_time', sa.String(length=50), nullable=False),
        sa.Column('timezone', sa.String(length=50), nullable=False, server_default='Asia/Kolkata'),
        sa.Column('start_date', sa.Date(), nullable=False),
        sa.Column('recurrence', sa.String(length=50), nullable=False, server_default='daily'),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'reminder_completions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('reminder_id', sa.Integer(), nullable=False),
        sa.Column('scheduled_occurrence', sa.DateTime(), nullable=False),
        sa.Column('is_completed', sa.Boolean(), nullable=False, server_default='1'),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('snoozed_until', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['reminder_id'], ['care_reminders.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # 10. conversations & chat_messages
    op.create_table(
        'conversations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('language', sa.String(length=10), nullable=False, server_default='en'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'chat_messages',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('conversation_id', sa.Integer(), nullable=False),
        sa.Column('role', sa.String(length=50), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # 11. consultation_briefs
    op.create_table(
        'consultation_briefs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('primary_concerns', sa.Text(), nullable=True),
        sa.Column('symptoms_summary', sa.Text(), nullable=True),
        sa.Column('lab_flags_summary', sa.Text(), nullable=True),
        sa.Column('prioritized_questions', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # 12. community_posts, community_replies, content_reports
    op.create_table(
        'community_posts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('pseudonym', sa.String(length=100), nullable=False, server_default='Anonymous Saathi'),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('tags', sa.String(length=255), nullable=True),
        sa.Column('helpful_votes', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('is_flagged', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='active'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'community_replies',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('post_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('pseudonym', sa.String(length=100), nullable=False, server_default='Anonymous Saathi'),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='active'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['post_id'], ['community_posts.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'content_reports',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('reporter_id', sa.Integer(), nullable=True),
        sa.Column('post_id', sa.Integer(), nullable=False),
        sa.Column('reason', sa.String(length=500), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='pending_review'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['post_id'], ['community_posts.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['reporter_id'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )

    # 13. notifications
    op.create_table(
        'notifications',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('message', sa.String(length=500), nullable=False),
        sa.Column('notification_type', sa.String(length=50), nullable=False, server_default='system'),
        sa.Column('is_read', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('notifications')
    op.drop_table('content_reports')
    op.drop_table('community_replies')
    op.drop_table('community_posts')
    op.drop_table('consultation_briefs')
    op.drop_table('chat_messages')
    op.drop_table('conversations')
    op.drop_table('reminder_completions')
    op.drop_table('care_reminders')
    op.drop_table('meal_plan_items')
    op.drop_table('meal_plans')
    op.drop_table('meal_items')
    op.drop_table('symptom_records')
    op.drop_table('cycle_records')
    op.drop_table('biomarkers')
    op.drop_table('medical_documents')
    op.drop_table('health_profiles')
    op.drop_table('users')
