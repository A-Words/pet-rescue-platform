"""initial tables, views, procedures, and triggers

Revision ID: 001
Revises:
Create Date: 2026-05-30

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # === TABLES ===

    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("username", sa.String(50), unique=True, nullable=False),
        sa.Column("email", sa.String(100), unique=True, nullable=False),
        sa.Column("hashed_password", sa.String(255), nullable=False),
        sa.Column("phone", sa.String(20)),
        sa.Column("avatar_url", sa.String(500)),
        sa.Column("role", sa.String(20), nullable=False, server_default="user"),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        "lost_pets",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("pet_name", sa.String(50), nullable=False),
        sa.Column("pet_type", sa.String(20), nullable=False),
        sa.Column("breed", sa.String(50)),
        sa.Column("color", sa.String(30)),
        sa.Column("gender", sa.String(10)),
        sa.Column("age_description", sa.String(50)),
        sa.Column("photo_urls", postgresql.ARRAY(sa.String)),
        sa.Column("description", sa.Text, nullable=False),
        sa.Column("lost_date", sa.Date, nullable=False),
        sa.Column("lost_location", sa.String(255), nullable=False),
        sa.Column("latitude", sa.Numeric(10, 7)),
        sa.Column("longitude", sa.Numeric(10, 7)),
        sa.Column("contact_info", sa.String(100), nullable=False),
        sa.Column("reward_amount", sa.Numeric(10, 2), server_default="0"),
        sa.Column("status", sa.String(20), nullable=False, server_default="active"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        "found_clues",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("lost_pet_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("lost_pets.id"), nullable=False),
        sa.Column("reporter_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("photo_urls", postgresql.ARRAY(sa.String)),
        sa.Column("description", sa.Text, nullable=False),
        sa.Column("found_location", sa.String(255), nullable=False),
        sa.Column("latitude", sa.Numeric(10, 7)),
        sa.Column("longitude", sa.Numeric(10, 7)),
        sa.Column("found_date", sa.Date, nullable=False),
        sa.Column("contact_info", sa.String(100), nullable=False),
        sa.Column("status", sa.String(20), nullable=False, server_default="pending"),
        sa.Column("admin_notes", sa.Text),
        sa.Column("reviewed_by", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id")),
        sa.Column("reviewed_at", sa.DateTime(timezone=True)),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        "adoptable_pets",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("pet_name", sa.String(50), nullable=False),
        sa.Column("pet_type", sa.String(20), nullable=False),
        sa.Column("breed", sa.String(50)),
        sa.Column("color", sa.String(30)),
        sa.Column("gender", sa.String(10)),
        sa.Column("age_months", sa.Integer),
        sa.Column("photo_urls", postgresql.ARRAY(sa.String)),
        sa.Column("description", sa.Text),
        sa.Column("health_status", sa.String(20), nullable=False, server_default="healthy"),
        sa.Column("is_vaccinated", sa.Boolean, nullable=False, server_default="false"),
        sa.Column("is_dewormed", sa.Boolean, nullable=False, server_default="false"),
        sa.Column("is_sterilized", sa.Boolean, nullable=False, server_default="false"),
        sa.Column("adoption_status", sa.String(20), nullable=False, server_default="available"),
        sa.Column("rescue_station", sa.String(100)),
        sa.Column("intake_date", sa.Date, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        "adoption_applications",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("pet_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("adoptable_pets.id"), nullable=False),
        sa.Column("applicant_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("applicant_name", sa.String(50), nullable=False),
        sa.Column("applicant_phone", sa.String(20), nullable=False),
        sa.Column("applicant_address", sa.String(255), nullable=False),
        sa.Column("applicant_id_number", sa.String(20), nullable=False),
        sa.Column("housing_type", sa.String(20)),
        sa.Column("has_other_pets", sa.Boolean, server_default="false"),
        sa.Column("adoption_reason", sa.Text, nullable=False),
        sa.Column("experience_description", sa.Text),
        sa.Column("status", sa.String(20), nullable=False, server_default="pending"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("pet_id", "applicant_id", name="uq_pet_applicant"),
    )

    op.create_table(
        "review_records",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("application_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("adoption_applications.id"), nullable=False),
        sa.Column("reviewer_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("decision", sa.String(20), nullable=False),
        sa.Column("review_notes", sa.Text),
        sa.Column("reviewed_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        "visit_reminders",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("application_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("adoption_applications.id"), nullable=False),
        sa.Column("adopter_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("pet_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("adoptable_pets.id"), nullable=False),
        sa.Column("reminder_date", sa.Date, nullable=False),
        sa.Column("visit_date", sa.Date),
        sa.Column("status", sa.String(20), nullable=False, server_default="pending"),
        sa.Column("visit_notes", sa.Text),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    # === INDEXES ===
    op.create_index("idx_lost_pets_user_id", "lost_pets", ["user_id"])
    op.create_index("idx_lost_pets_status", "lost_pets", ["status"])
    op.create_index("idx_lost_pets_lost_date", "lost_pets", ["lost_date"])
    op.create_index("idx_found_clues_lost_pet_id", "found_clues", ["lost_pet_id"])
    op.create_index("idx_found_clues_reporter_id", "found_clues", ["reporter_id"])
    op.create_index("idx_adoptable_pets_type", "adoptable_pets", ["pet_type"])
    op.create_index("idx_adoptable_pets_status", "adoptable_pets", ["adoption_status"])
    op.create_index("idx_adoption_applications_pet_id", "adoption_applications", ["pet_id"])
    op.create_index("idx_adoption_applications_applicant_id", "adoption_applications", ["applicant_id"])
    op.create_index("idx_adoption_applications_status", "adoption_applications", ["status"])
    op.create_index("idx_visit_reminders_reminder_date", "visit_reminders", ["reminder_date"])
    op.create_index("idx_visit_reminders_status", "visit_reminders", ["status"])

    # === VIEW ===
    op.execute("""
        CREATE OR REPLACE VIEW v_adoptable_pets AS
        SELECT
            ap.id, ap.pet_name, ap.pet_type, ap.breed, ap.color, ap.gender,
            ap.age_months, ap.photo_urls, ap.description, ap.health_status,
            ap.is_vaccinated, ap.is_dewormed, ap.is_sterilized,
            ap.rescue_station, ap.intake_date,
            COALESCE(app_count.application_count, 0) AS application_count
        FROM adoptable_pets ap
        LEFT JOIN (
            SELECT pet_id, COUNT(*) AS application_count
            FROM adoption_applications
            WHERE status = 'pending'
            GROUP BY pet_id
        ) app_count ON ap.id = app_count.pet_id
        WHERE ap.adoption_status = 'available';
    """)

    # === STORED PROCEDURE ===
    op.execute("""
        CREATE OR REPLACE FUNCTION sp_monthly_statistics(p_year INTEGER, p_month INTEGER)
        RETURNS TABLE (
            total_lost_reports BIGINT,
            successful_recoveries BIGINT,
            recovery_rate NUMERIC(5,2),
            total_adoption_applications BIGINT,
            approved_adoptions BIGINT,
            adoption_success_rate NUMERIC(5,2),
            total_found_clues BIGINT,
            confirmed_clues BIGINT
        ) AS $$
        BEGIN
            RETURN QUERY
            SELECT
                (SELECT COUNT(*) FROM lost_pets
                 WHERE EXTRACT(YEAR FROM created_at) = p_year
                   AND EXTRACT(MONTH FROM created_at) = p_month) AS total_lost_reports,
                (SELECT COUNT(*) FROM lost_pets
                 WHERE EXTRACT(YEAR FROM created_at) = p_year
                   AND EXTRACT(MONTH FROM created_at) = p_month
                   AND status = 'found') AS successful_recoveries,
                CASE
                    WHEN (SELECT COUNT(*) FROM lost_pets
                          WHERE EXTRACT(YEAR FROM created_at) = p_year
                            AND EXTRACT(MONTH FROM created_at) = p_month) = 0 THEN 0
                    ELSE ROUND(
                        (SELECT COUNT(*)::NUMERIC FROM lost_pets
                         WHERE EXTRACT(YEAR FROM created_at) = p_year
                           AND EXTRACT(MONTH FROM created_at) = p_month
                           AND status = 'found') /
                        (SELECT COUNT(*)::NUMERIC FROM lost_pets
                         WHERE EXTRACT(YEAR FROM created_at) = p_year
                           AND EXTRACT(MONTH FROM created_at) = p_month) * 100, 2)
                END AS recovery_rate,
                (SELECT COUNT(*) FROM adoption_applications
                 WHERE EXTRACT(YEAR FROM created_at) = p_year
                   AND EXTRACT(MONTH FROM created_at) = p_month) AS total_adoption_applications,
                (SELECT COUNT(*) FROM adoption_applications
                 WHERE EXTRACT(YEAR FROM created_at) = p_year
                   AND EXTRACT(MONTH FROM created_at) = p_month
                   AND status = 'approved') AS approved_adoptions,
                CASE
                    WHEN (SELECT COUNT(*) FROM adoption_applications
                          WHERE EXTRACT(YEAR FROM created_at) = p_year
                            AND EXTRACT(MONTH FROM created_at) = p_month) = 0 THEN 0
                    ELSE ROUND(
                        (SELECT COUNT(*)::NUMERIC FROM adoption_applications
                         WHERE EXTRACT(YEAR FROM created_at) = p_year
                           AND EXTRACT(MONTH FROM created_at) = p_month
                           AND status = 'approved') /
                        (SELECT COUNT(*)::NUMERIC FROM adoption_applications
                         WHERE EXTRACT(YEAR FROM created_at) = p_year
                           AND EXTRACT(MONTH FROM created_at) = p_month) * 100, 2)
                END AS adoption_success_rate,
                (SELECT COUNT(*) FROM found_clues
                 WHERE EXTRACT(YEAR FROM created_at) = p_year
                   AND EXTRACT(MONTH FROM created_at) = p_month) AS total_found_clues,
                (SELECT COUNT(*) FROM found_clues
                 WHERE EXTRACT(YEAR FROM created_at) = p_year
                   AND EXTRACT(MONTH FROM created_at) = p_month
                   AND status = 'confirmed') AS confirmed_clues;
        END;
        $$ LANGUAGE plpgsql;
    """)

    # === TRIGGERS ===

    # Trigger function: auto-update updated_at
    op.execute("""
        CREATE OR REPLACE FUNCTION fn_update_timestamp()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = now();
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)

    for table in ["users", "lost_pets", "adoptable_pets", "adoption_applications"]:
        op.execute(f"""
            CREATE TRIGGER trg_{table}_updated_at
            BEFORE UPDATE ON {table}
            FOR EACH ROW EXECUTE FUNCTION fn_update_timestamp();
        """)

    # Trigger function: on adoption approved
    op.execute("""
        CREATE OR REPLACE FUNCTION fn_on_adoption_approved()
        RETURNS TRIGGER AS $$
        BEGIN
            IF NEW.status = 'approved' AND (OLD.status IS NULL OR OLD.status != 'approved') THEN
                UPDATE adoptable_pets SET adoption_status = 'adopted', updated_at = now()
                WHERE id = NEW.pet_id;
                UPDATE adoption_applications SET status = 'rejected', updated_at = now()
                WHERE pet_id = NEW.pet_id AND id != NEW.id AND status = 'pending';
            END IF;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)

    op.execute("""
        CREATE TRIGGER trg_adoption_approved
        AFTER UPDATE OF status ON adoption_applications
        FOR EACH ROW EXECUTE FUNCTION fn_on_adoption_approved();
    """)

    # Trigger function: check duplicate application
    op.execute("""
        CREATE OR REPLACE FUNCTION fn_check_duplicate_application()
        RETURNS TRIGGER AS $$
        BEGIN
            IF EXISTS (
                SELECT 1 FROM adoption_applications
                WHERE pet_id = NEW.pet_id
                  AND applicant_id = NEW.applicant_id
                  AND status IN ('pending', 'approved')
            ) THEN
                RAISE EXCEPTION 'Duplicate application: user has already applied for this pet'
                    USING ERRCODE = 'unique_violation';
            END IF;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)

    op.execute("""
        CREATE TRIGGER trg_check_duplicate_application
        BEFORE INSERT ON adoption_applications
        FOR EACH ROW EXECUTE FUNCTION fn_check_duplicate_application();
    """)

    # Trigger function: generate visit reminders
    op.execute("""
        CREATE OR REPLACE FUNCTION fn_generate_visit_reminders()
        RETURNS TRIGGER AS $$
        BEGIN
            IF NEW.status = 'approved' AND (OLD.status IS NULL OR OLD.status != 'approved') THEN
                INSERT INTO visit_reminders (application_id, adopter_id, pet_id, reminder_date, status)
                VALUES (NEW.id, NEW.applicant_id, NEW.pet_id, CURRENT_DATE + INTERVAL '7 days', 'pending');
                INSERT INTO visit_reminders (application_id, adopter_id, pet_id, reminder_date, status)
                VALUES (NEW.id, NEW.applicant_id, NEW.pet_id, CURRENT_DATE + INTERVAL '30 days', 'pending');
                INSERT INTO visit_reminders (application_id, adopter_id, pet_id, reminder_date, status)
                VALUES (NEW.id, NEW.applicant_id, NEW.pet_id, CURRENT_DATE + INTERVAL '90 days', 'pending');
            END IF;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)

    op.execute("""
        CREATE TRIGGER trg_generate_visit_reminders
        AFTER UPDATE OF status ON adoption_applications
        FOR EACH ROW EXECUTE FUNCTION fn_generate_visit_reminders();
    """)


def downgrade() -> None:
    # Drop triggers
    op.execute("DROP TRIGGER IF EXISTS trg_generate_visit_reminders ON adoption_applications;")
    op.execute("DROP TRIGGER IF EXISTS trg_check_duplicate_application ON adoption_applications;")
    op.execute("DROP TRIGGER IF EXISTS trg_adoption_approved ON adoption_applications;")
    for table in ["users", "lost_pets", "adoptable_pets", "adoption_applications"]:
        op.execute(f"DROP TRIGGER IF EXISTS trg_{table}_updated_at ON {table};")

    # Drop trigger functions
    op.execute("DROP FUNCTION IF EXISTS fn_generate_visit_reminders();")
    op.execute("DROP FUNCTION IF EXISTS fn_check_duplicate_application();")
    op.execute("DROP FUNCTION IF EXISTS fn_on_adoption_approved();")
    op.execute("DROP FUNCTION IF EXISTS fn_update_timestamp();")

    # Drop stored procedure
    op.execute("DROP FUNCTION IF EXISTS sp_monthly_statistics(INTEGER, INTEGER);")

    # Drop view
    op.execute("DROP VIEW IF EXISTS v_adoptable_pets;")

    # Drop indexes
    op.drop_index("idx_visit_reminders_status")
    op.drop_index("idx_visit_reminders_reminder_date")
    op.drop_index("idx_adoption_applications_status")
    op.drop_index("idx_adoption_applications_applicant_id")
    op.drop_index("idx_adoption_applications_pet_id")
    op.drop_index("idx_adoptable_pets_status")
    op.drop_index("idx_adoptable_pets_type")
    op.drop_index("idx_found_clues_reporter_id")
    op.drop_index("idx_found_clues_lost_pet_id")
    op.drop_index("idx_lost_pets_lost_date")
    op.drop_index("idx_lost_pets_status")
    op.drop_index("idx_lost_pets_user_id")

    # Drop tables
    op.drop_table("visit_reminders")
    op.drop_table("review_records")
    op.drop_table("adoption_applications")
    op.drop_table("adoptable_pets")
    op.drop_table("found_clues")
    op.drop_table("lost_pets")
    op.drop_table("users")
