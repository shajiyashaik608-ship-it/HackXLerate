from datetime import date, timedelta, datetime
from sqlalchemy.orm import Session
from app.db.session import engine, SessionLocal
from app.db.base import Base
from app.core.config import settings
from app.core.security import get_password_hash
from app.core.logging import logger
from app.models.user import User
from app.models.profile import HealthProfile
from app.models.document import MedicalDocument
from app.models.biomarker import Biomarker
from app.models.cycle import CycleRecord
from app.models.symptom import SymptomRecord
from app.models.reminder import CareReminder
from app.models.community import CommunityPost, CommunityReply
from app.models.notification import Notification
from app.services.nutrition_service import nutrition_service


def seed_demo_data(db: Session):
    """
    Seeds clearly-labelled fictional demonstration records for hackathon evaluation.
    Never seeds into production without explicit DEMO_MODE activation.
    """
    logger.info("Initializing synthetic demonstration dataset...")

    # Ensure tables exist
    Base.metadata.create_all(bind=engine)

    # 1. Seed 10 Indian nutritional meals
    nutrition_service.ensure_default_meals_seeded(db)

    # 2. Check if demo user already exists
    demo_email = settings.DEMO_USER_EMAIL.lower().strip()
    existing_user = db.query(User).filter(User.email == demo_email).first()

    if existing_user:
        logger.info(f"Demo user '{demo_email}' already exists. Skipping duplicate seeding.")
        return existing_user

    # Create demo user
    demo_user = User(
        email=demo_email,
        hashed_password=get_password_hash(settings.DEMO_USER_PASSWORD),
        full_name="Priya Sharma (Synthetic Demo Profile)",
        is_active=True,
        is_verified=True,
        consent_given=True
    )
    db.add(demo_user)
    db.commit()
    db.refresh(demo_user)

    # 3. Create HealthProfile
    profile = HealthProfile(
        user_id=demo_user.id,
        age=26,
        diet_type="veg",
        baseline_cycle_length=35,
        period_duration=5,
        wellness_goals="Regulate menstrual cycle variability, improve insulin sensitivity, eat balanced regional Indian foods.",
        allergies="None reported",
        preferred_language="en",
        timezone="Asia/Kolkata"
    )
    db.add(profile)

    # 4. Two sample medical reports
    doc1 = MedicalDocument(
        user_id=demo_user.id,
        file_name="Synthetic_Thyroid_Metabolic_Report.pdf",
        file_type="pdf",
        file_path="demo_storage/Synthetic_Thyroid_Metabolic_Report.pdf",
        category="lab_report",
        processing_status="completed",
        ocr_raw_text="Thyroid Profile & Metabolic Screen\nTSH: 4.8 mIU/L (Ref: 0.4 - 4.5)\nFasting Insulin: 18.4 uIU/mL (Ref: 2.0 - 24.9)",
        upload_date=date.today() - timedelta(days=20)
    )
    db.add(doc1)
    db.commit()
    db.refresh(doc1)

    bio1 = Biomarker(
        user_id=demo_user.id,
        document_id=doc1.id,
        test_name="TSH",
        observed_value="4.8",
        numeric_value=4.8,
        unit="mIU/L",
        reference_range_lower=0.4,
        reference_range_upper=4.5,
        reference_range_text="0.4 - 4.5 mIU/L",
        status="elevated",
        test_date=date.today() - timedelta(days=21),
        extraction_confidence=0.95,
        source_page=1,
        plain_explanation="Thyroid Stimulating Hormone. Observed slightly above the lab's reference limit. Often reviewed for ovulatory impact.",
        is_user_corrected=False
    )
    bio2 = Biomarker(
        user_id=demo_user.id,
        document_id=doc1.id,
        test_name="Fasting Insulin",
        observed_value="18.4",
        numeric_value=18.4,
        unit="uIU/mL",
        reference_range_lower=2.0,
        reference_range_upper=24.9,
        reference_range_text="2.0 - 24.9 uIU/mL",
        status="normal",
        test_date=date.today() - timedelta(days=21),
        extraction_confidence=0.95,
        source_page=1,
        plain_explanation="Fasting Insulin within broad reference limits, though monitored for metabolic and glycemic stability.",
        is_user_corrected=False
    )
    db.add_all([bio1, bio2])

    doc2 = MedicalDocument(
        user_id=demo_user.id,
        file_name="Synthetic_Reproductive_Hormone_Panel.pdf",
        file_type="pdf",
        file_path="demo_storage/Synthetic_Reproductive_Hormone_Panel.pdf",
        category="lab_report",
        processing_status="completed",
        ocr_raw_text="Hormone Panel\nLH: 9.8 mIU/mL (Ref: 1.9 - 12.5)\nFSH: 4.9 mIU/mL (Ref: 2.5 - 10.2)\nTotal Testosterone: 52 ng/dL (Ref: 15 - 70)",
        upload_date=date.today() - timedelta(days=5)
    )
    db.add(doc2)
    db.commit()
    db.refresh(doc2)

    bio3 = Biomarker(
        user_id=demo_user.id,
        document_id=doc2.id,
        test_name="LH",
        observed_value="9.8",
        numeric_value=9.8,
        unit="mIU/mL",
        reference_range_lower=1.9,
        reference_range_upper=12.5,
        reference_range_text="1.9 - 12.5 mIU/mL",
        status="normal",
        test_date=date.today() - timedelta(days=6),
        extraction_confidence=0.92,
        source_page=1,
        plain_explanation="Luteinizing Hormone signals ovarian ovulation. LH to FSH ratio of approximately 2:1 is common in PCOS.",
        is_user_corrected=False
    )
    bio4 = Biomarker(
        user_id=demo_user.id,
        document_id=doc2.id,
        test_name="FSH",
        observed_value="4.9",
        numeric_value=4.9,
        unit="mIU/mL",
        reference_range_lower=2.5,
        reference_range_upper=10.2,
        reference_range_text="2.5 - 10.2 mIU/mL",
        status="normal",
        test_date=date.today() - timedelta(days=6),
        extraction_confidence=0.92,
        source_page=1,
        plain_explanation="Follicle Stimulating Hormone fosters egg follicle development.",
        is_user_corrected=False
    )
    bio5 = Biomarker(
        user_id=demo_user.id,
        document_id=doc2.id,
        test_name="Total Testosterone",
        observed_value="52",
        numeric_value=52.0,
        unit="ng/dL",
        reference_range_lower=15.0,
        reference_range_upper=70.0,
        reference_range_text="15 - 70 ng/dL",
        status="normal",
        test_date=date.today() - timedelta(days=6),
        extraction_confidence=0.90,
        source_page=1,
        plain_explanation="Primary androgen hormone. Modest elevations in androgen levels contribute to acne or cycle variability.",
        is_user_corrected=False
    )
    db.add_all([bio3, bio4, bio5])

    # 5. Four historical cycle records with varying intervals
    today = date.today()
    c1 = CycleRecord(
        user_id=demo_user.id,
        start_date=today - timedelta(days=125),
        end_date=today - timedelta(days=120),
        duration_days=5,
        flow_intensity="medium",
        notes="Moderate cramps on day 1."
    )
    c2 = CycleRecord(
        user_id=demo_user.id,
        start_date=today - timedelta(days=88),
        end_date=today - timedelta(days=83),
        duration_days=5,
        flow_intensity="heavy",
        notes="Heavier flow than usual."
    )
    c3 = CycleRecord(
        user_id=demo_user.id,
        start_date=today - timedelta(days=53),
        end_date=today - timedelta(days=49),
        duration_days=4,
        flow_intensity="medium",
        notes="Cycle interval was 35 days."
    )
    c4 = CycleRecord(
        user_id=demo_user.id,
        start_date=today - timedelta(days=16),
        end_date=today - timedelta(days=12),
        duration_days=4,
        flow_intensity="light",
        notes="Latest recorded cycle start."
    )
    db.add_all([c1, c2, c3, c4])

    # 6. Sample symptom records
    s1 = SymptomRecord(
        user_id=demo_user.id,
        recorded_date=today - timedelta(days=15),
        symptom_type="cramps",
        severity="mild",
        notes="Lower abdominal fullness on period onset."
    )
    s2 = SymptomRecord(
        user_id=demo_user.id,
        recorded_date=today - timedelta(days=7),
        symptom_type="acne",
        severity="moderate",
        notes="Mild jawline flare-up."
    )
    s3 = SymptomRecord(
        user_id=demo_user.id,
        recorded_date=today - timedelta(days=2),
        symptom_type="bloating",
        severity="mild",
        notes="Felt bloated after dinner."
    )
    db.add_all([s1, s2, s3])

    # 7. Three care reminders
    r1 = CareReminder(
        user_id=demo_user.id,
        title="Myo-Inositol & Folate Supplement",
        category="medication",
        scheduled_time="08:30",
        timezone="Asia/Kolkata",
        start_date=today - timedelta(days=30),
        recurrence="daily",
        notes="User-confirmed daily supplement as discussed with doctor.",
        is_active=True
    )
    r2 = CareReminder(
        user_id=demo_user.id,
        title="Soaked Methi & Warm Water Routine",
        category="hydration",
        scheduled_time="07:00",
        timezone="Asia/Kolkata",
        start_date=today - timedelta(days=30),
        recurrence="daily",
        notes="Morning hydration support for insulin sensitivity.",
        is_active=True
    )
    r3 = CareReminder(
        user_id=demo_user.id,
        title="Gynecologist Follow-Up Consultation",
        category="appointment",
        scheduled_time="10:30",
        timezone="Asia/Kolkata",
        start_date=today + timedelta(days=7),
        recurrence="once",
        notes="Bring printable consultation brief and recent thyroid lab report.",
        is_active=True
    )
    db.add_all([r1, r2, r3])

    # 8. Four educational community posts
    p1 = CommunityPost(
        user_id=None,
        pseudonym="HyderabadSaathi",
        title="How switching from white rice to Korralu helped my energy levels",
        content="I was feeling extreme mid-day sluggishness after heavy white rice lunches. My doctor suggested trying foxtail millet (Korralu) paired with palak dal and curd. It has made a huge difference to my afternoon focus!",
        tags="diet,millets,energy",
        status="active"
    )
    p2 = CommunityPost(
        user_id=None,
        pseudonym="BangaloreWarrior",
        title="PCOS Friendly Breakfast: Moong Dal Pesarattu Recipe",
        content="Whole moong dal soaked overnight and ground with ginger and green chillies makes the best high-protein breakfast. It keeps me satisfied until 1 PM without sugar crashes.",
        tags="recipes,breakfast,protein",
        status="active"
    )
    p3 = CommunityPost(
        user_id=None,
        pseudonym="Ananya_K",
        title="What questions helped you most during your gynecologist visit?",
        content="Writing down my symptoms and bringing my lab dates made a world of difference. The doctor took all my concerns much more seriously when I handed over a concise printed summary.",
        tags="doctor,consultation,advocacy",
        status="active"
    )
    p4 = CommunityPost(
        user_id=None,
        pseudonym="GentleMover",
        title="Gentle 20-minute post-dinner walks for insulin sensitivity",
        content="You don't have to do intense HIIT every day! Even a relaxing 15-20 minute stroll after dinner helps muscles uptake glucose and supports restful sleep.",
        tags="movement,lifestyle,habits",
        status="active"
    )
    db.add_all([p1, p2, p3, p4])

    # 9. Notification
    notif = Notification(
        user_id=demo_user.id,
        title="Doctor Visit Preparation Ready",
        message="Your recent lab values and cycle dates have been organized into your printable consultation brief.",
        notification_type="system",
        is_read=False
    )
    db.add(notif)

    db.commit()
    logger.info("Successfully seeded synthetic demonstration data for Health Saathi.")
    return demo_user


if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_demo_data(db)
        print("Database initialization and demo seeding complete.")
    finally:
        db.close()
