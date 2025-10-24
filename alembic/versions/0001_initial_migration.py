"""initial async medisafe db"""

from alembic import op
import sqlalchemy as sa
import uuid

revision = "0001_initial_migration"
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("uuid", sa.dialects.postgresql.UUID(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4),
        sa.Column("hash_password", sa.Text, nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True), onupdate=sa.func.now()),
    )

    op.create_table(
        "user_relations",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("friend_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "schedules",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("start_date", sa.Date, nullable=False),
        sa.Column("duration_days", sa.Integer, server_default="0"),
        sa.Column("schedule_type", sa.Enum("daily", "weekly_days", "cycle", "every_x_days", name="scheduletype"), nullable=False),
        sa.Column("days_of_week", sa.ARRAY(sa.Integer)),
        sa.Column("cycle_on", sa.Integer),
        sa.Column("cycle_off", sa.Integer),
        sa.Column("every_x_days", sa.Integer),
        sa.Column("every_x_weeks", sa.Integer),
        sa.Column("times_per_day", sa.Integer, nullable=False),
        sa.Column("time_list", sa.ARRAY(sa.Time)),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.func.now()),
        sa.CheckConstraint("times_per_day <= 6"),
        sa.CheckConstraint("duration_days <= 3650"),
        sa.CheckConstraint("cycle_on <= 60"),
        sa.CheckConstraint("cycle_off <= 60"),
        sa.CheckConstraint("every_x_days <= 30"),
    )

    op.create_table(
        "medicines",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("patient_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("schedules_id", sa.Integer, sa.ForeignKey("schedules.id", ondelete="CASCADE"), nullable=False),
        sa.Column("name", sa.Text, nullable=False),
        sa.Column("form", sa.Enum("tablet", "drop", "spray", "solution", "injection", "powder", "inhaler", "other", name="medicineform"), nullable=False),
        sa.Column("unit", sa.Enum("mg", "g", "pcs", "ml", "caps.", "dose", name="medicineunit"), nullable=False),
        sa.Column("dosage", sa.Float, nullable=False),
        sa.Column("instructions", sa.Text),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "intake_history",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("medicine_id", sa.Integer, sa.ForeignKey("medicines.id", ondelete="CASCADE"), nullable=False),
        sa.Column("patient_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("planned_time", sa.Time),
        sa.Column("datetime", sa.TIMESTAMP(timezone=True)),
        sa.Column("taken", sa.Boolean, server_default="false"),
        sa.Column("skipped", sa.Boolean, server_default="false"),
        sa.Column("dose_taken", sa.Float),
        sa.Column("synced", sa.Boolean, server_default="false"),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.func.now()),
    )

def downgrade() -> None:
    op.drop_table("intake_history")
    op.drop_table("medicines")
    op.drop_table("schedules")
    op.drop_table("user_relations")
    op.drop_table("users")
