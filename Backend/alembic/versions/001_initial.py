"""initial migration

Revision ID: 001
Revises:
Create Date: 2026-08-14

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("username", sa.String(50), nullable=False),
        sa.Column("password", sa.String(255), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("username"),
    )

    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(500), nullable=False),
        sa.Column("category", sa.String(200), nullable=False),
        sa.Column("price", sa.Float(), nullable=False),
        sa.Column("rating", sa.Float(), nullable=False),
        sa.Column("number_of_reviews", sa.Integer(), nullable=False),
        sa.Column("product_url", sa.String(), nullable=False),
        sa.Column("image_url", sa.String(), nullable=False),
        sa.Column("score", sa.Integer(), nullable=True),
        sa.Column("reasoning", sa.Text(), nullable=True),
        sa.Column("trend_score", sa.Float(), nullable=True),
        sa.Column("boost_score", sa.Float(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=True,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.CheckConstraint("price >= 0", name="check_price_non_negative"),
        sa.CheckConstraint(
            "rating >= 0 AND rating <= 5", name="check_rating_range"
        ),
        sa.CheckConstraint(
            "number_of_reviews >= 0", name="check_reviews_non_negative"
        ),
        sa.CheckConstraint(
            "score >= 0 AND score <= 100", name="check_score_range"
        ),
    )

    op.create_table(
        "sales_history",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(500), nullable=False),
        sa.Column("category", sa.String(200), nullable=False),
        sa.Column("price", sa.Float(), nullable=False),
        sa.Column("rating", sa.Float(), nullable=True),
        sa.Column("number_of_reviews", sa.Integer(), nullable=True),
        sa.Column("product_url", sa.String(), nullable=True),
        sa.Column("image_url", sa.String(), nullable=True),
        sa.Column("keywords", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("sales_history")
    op.drop_table("products")
    op.drop_table("users")
