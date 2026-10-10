import sys, os
from datetime import date, datetime, timedelta

# Ensure backend package can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../backend")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../ai-ml")))

from app.database import SessionLocal, Base, engine
from app.models.user import User
from app.models.medical_report import MedicalReport
from app.models.cycle_record import CycleRecord
from app.models.reminder import Reminder
from app.models.food_preference import FoodPreference
from app.models.community_post import CommunityPost
from app.utils.security import get_password_hash

def seed():
    print("Seeding synthetic test data for Hackathon demo...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # 1. Create or get demo user
    demo_email = "priya.sharma@example.com"
    user = db.query(User).filter(User.email == demo_email).first()
    if not user:
        user = User(
            email=demo_email,
            hashed_password=get_password_hash("demo1234"),
            full_name="Priya Sharma",
            preferred_language="te",
            consent_given=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        print(f"Created demo user: {user.email}")

    # 2. Seed Medical Reports
    if db.query(MedicalReport).filter(MedicalReport.user_id == user.id).count() == 0:
        rep1 = MedicalReport(
            user_id=user.id,
            title="Thyroid & Fasting Glucose Profile",
            report_type="blood_test",
            file_path="thyroid_panel_oct.pdf",
            extracted_text="TSH: 4.8 mIU/L (Ref: 0.4 - 4.5), Fasting Insulin: 18.2 uIU/mL (Ref: 2.0 - 24.9), HbA1c: 5.4% (Ref: 4.0 - 5.6%)",
            structured_data=[
                {
                    "test_name": "TSH (Thyroid)",
                    "value": "4.8",
                    "unit": "mIU/L",
                    "reference_range": "0.4 - 4.5 mIU/L",
                    "status": "elevated",
                    "plain_explanation": "TSH is slightly high, suggesting subclinical thyroid slowing that can affect menstrual regularity."
                },
                {
                    "test_name": "Fasting Insulin",
                    "value": "18.2",
                    "unit": "uIU/mL",
                    "reference_range": "2.0 - 24.9 uIU/mL",
                    "status": "normal",
                    "plain_explanation": "In upper normal range. Often tracked in PCOS to monitor cellular insulin sensitivity."
                },
                {
                    "test_name": "HbA1c",
                    "value": "5.4",
                    "unit": "%",
                    "reference_range": "4.0 - 5.6%",
                    "status": "normal",
                    "plain_explanation": "Healthy average 3-month blood glucose level."
                }
            ],
            explanation=(
                "Summary: 3 tests analyzed. TSH is mildly elevated above laboratory standard (4.8 mIU/L). "
                "Fasting insulin and HbA1c remain within expected reference boundaries. "
                "Recommended for clinical follow-up during your next consultation."
            )
        )
        db.add(rep1)
        print("Added sample lab report.")

    # 3. Seed Cycle Records
    if db.query(CycleRecord).filter(CycleRecord.user_id == user.id).count() == 0:
        c1 = CycleRecord(
            user_id=user.id,
            start_date=date.today() - timedelta(days=52),
            end_date=date.today() - timedelta(days=47),
            flow_intensity="moderate",
            symptoms=["cramps", "fatigue", "mood_swings"],
            notes="Cycle started after 38 days gap."
        )
        c2 = CycleRecord(
            user_id=user.id,
            start_date=date.today() - timedelta(days=14),
            end_date=date.today() - timedelta(days=10),
            flow_intensity="light",
            symptoms=["acne", "bloating"],
            notes="Short duration, light spotting on day 4."
        )
        db.add_all([c1, c2])
        print("Added sample cycle records.")

    # 4. Seed Reminders
    if db.query(Reminder).filter(Reminder.user_id == user.id).count() == 0:
        r1 = Reminder(
            user_id=user.id,
            title="Myo-Inositol & Folic Acid",
            reminder_type="medication",
            dosage="1 sachet dissolved in water",
            time_of_day="08:30",
            frequency="daily"
        )
        r2 = Reminder(
            user_id=user.id,
            title="Evening Walk & Hydration",
            reminder_type="lifestyle",
            dosage="30 mins brisk movement",
            time_of_day="18:00",
            frequency="daily"
        )
        db.add_all([r1, r2])
        print("Added sample reminders.")

    # 5. Seed Community Posts
    if db.query(CommunityPost).count() == 0:
        p1 = CommunityPost(
            user_id=user.id,
            author_alias="Anonymous Saathi",
            title="Best ways to manage dairy cravings with South Indian breakfast?",
            content="I used to have tea with cow milk and curd every morning. What are good substitutes that support insulin levels?",
            tag="nutrition",
            moderation_status="approved",
            answers=[
                {
                    "author": "Clinical Dietitian (Verified Educator)",
                    "text": "You can try small quantities of fermented curd (which has lower lactose) or switch to almond milk for chai. Pairing with whole moong pesarattu keeps your sugar steady."
                }
            ]
        )
        p2 = CommunityPost(
            user_id=user.id,
            author_alias="Sunitha K.",
            title="పీరియడ్స్ ఆలస్యం అయినప్పుడు ఎలాంటి యోగాసనాలు మేలు చేస్తాయి?",
            content="PCOS లో సహజంగా పీరియడ్స్ క్రమబద్ధం కావడానికి బటర్‌ఫ్లై పోజ్ (Baddha Konasana) పనికొస్తుందా?",
            tag="lifestyle",
            moderation_status="approved",
            answers=[
                {
                    "author": "Health Saathi Team",
                    "text": "అవును, బద్ధకోణాసనం మరియు సుప్త బద్ధకోణాసనం పెల్విక్ ప్రాంతంలో రక్తప్రసరణను మెరుగుపరుస్తాయి. రోజుకు 15 నిమిషాలు సాధన చేయడం ప్రయోజనకరం."
                }
            ]
        )
        db.add_all([p1, p2])
        print("Added sample community posts.")

    db.commit()
    db.close()
    print("Database seeding completed successfully!")

if __name__ == "__main__":
    seed()
