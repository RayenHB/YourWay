"""add perf indexes for orders and cases

Revision ID: 9b3d2f7c1a11
Revises: f306f12a40ca
Create Date: 2026-03-23 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "9b3d2f7c1a11"
down_revision: Union[str, None] = "7eed95fd2dc4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE INDEX IF NOT EXISTS ix_orders_created_at ON orders (created_at)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_orders_phone_case_id ON orders (phone_case_id)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_phone_cases_phone_model_id ON phone_cases (phone_model_id)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_phone_cases_case_type_id ON phone_cases (case_type_id)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_phone_case_templates_phone_case_id ON phone_case_templates (phone_case_id)")

    op.execute("CREATE INDEX IF NOT EXISTS ix_used_phone_cases_phone_model_id ON used_phone_cases (phone_model_id)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_used_phone_cases_case_type_id ON used_phone_cases (case_type_id)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_used_phone_case_templates_phone_case_id ON used_phone_case_templates (phone_case_id)")


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_used_phone_case_templates_phone_case_id")
    op.execute("DROP INDEX IF EXISTS ix_used_phone_cases_case_type_id")
    op.execute("DROP INDEX IF EXISTS ix_used_phone_cases_phone_model_id")

    op.execute("DROP INDEX IF EXISTS ix_phone_case_templates_phone_case_id")
    op.execute("DROP INDEX IF EXISTS ix_phone_cases_case_type_id")
    op.execute("DROP INDEX IF EXISTS ix_phone_cases_phone_model_id")
    op.execute("DROP INDEX IF EXISTS ix_orders_phone_case_id")
    op.execute("DROP INDEX IF EXISTS ix_orders_created_at")
