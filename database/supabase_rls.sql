-- ==============================================================================
-- Health Saathi (PCOS Saathi) - Supabase PostgreSQL Row Level Security (RLS)
-- ==============================================================================
-- This script configures production-grade Row Level Security on all Health Saathi
-- tables in Supabase PostgreSQL to prevent unauthorized and cross-user data access.
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- 1. Enable Row Level Security (RLS) on all tables
-- ------------------------------------------------------------------------------
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE health_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE medical_documents ENABLE ROW LEVEL SECURITY;
ALTER TABLE biomarkers ENABLE ROW LEVEL SECURITY;
ALTER TABLE cycle_records ENABLE ROW LEVEL SECURITY;
ALTER TABLE symptom_records ENABLE ROW LEVEL SECURITY;
ALTER TABLE meal_items ENABLE ROW LEVEL SECURITY;
ALTER TABLE meal_plans ENABLE ROW LEVEL SECURITY;
ALTER TABLE meal_plan_items ENABLE ROW LEVEL SECURITY;
ALTER TABLE care_reminders ENABLE ROW LEVEL SECURITY;
ALTER TABLE reminder_completions ENABLE ROW LEVEL SECURITY;
ALTER TABLE conversations ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE consultation_briefs ENABLE ROW LEVEL SECURITY;
ALTER TABLE community_posts ENABLE ROW LEVEL SECURITY;
ALTER TABLE community_replies ENABLE ROW LEVEL SECURITY;
ALTER TABLE content_reports ENABLE ROW LEVEL SECURITY;
ALTER TABLE notifications ENABLE ROW LEVEL SECURITY;

-- ------------------------------------------------------------------------------
-- 2. Service Role & Application Engine Bypass Policy
-- The FastAPI backend connects with application credentials and enforces
-- strict application-layer authorization, sanitization, and audit controls.
-- ------------------------------------------------------------------------------
CREATE POLICY "service_role_all_users" ON users FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "service_role_all_profiles" ON health_profiles FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "service_role_all_docs" ON medical_documents FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "service_role_all_biomarkers" ON biomarkers FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "service_role_all_cycles" ON cycle_records FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "service_role_all_symptoms" ON symptom_records FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "service_role_all_meals" ON meal_items FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "service_role_all_meal_plans" ON meal_plans FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "service_role_all_meal_plan_items" ON meal_plan_items FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "service_role_all_reminders" ON care_reminders FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "service_role_all_completions" ON reminder_completions FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "service_role_all_conversations" ON conversations FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "service_role_all_chat_messages" ON chat_messages FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "service_role_all_briefs" ON consultation_briefs FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "service_role_all_community_posts" ON community_posts FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "service_role_all_community_replies" ON community_replies FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "service_role_all_content_reports" ON content_reports FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "service_role_all_notifications" ON notifications FOR ALL TO service_role USING (true) WITH CHECK (true);

-- ------------------------------------------------------------------------------
-- 3. Authenticated Patient Policies (Direct Client / PostgREST Data API Access)
-- If accessed directly via Supabase Auth JWT, access is strictly scoped to the
-- authenticated patient's user_id or email claim.
-- ------------------------------------------------------------------------------

-- Helper expression for matching user id or email:
-- auth.uid()::text = user_id::text OR auth.jwt() ->> 'email' = (SELECT email FROM users WHERE id = user_id)

-- Users table: users can read and update only their own profile
CREATE POLICY "users_select_own" ON users FOR SELECT TO authenticated
    USING (auth.uid()::text = id::text OR auth.jwt() ->> 'email' = email);

CREATE POLICY "users_update_own" ON users FOR UPDATE TO authenticated
    USING (auth.uid()::text = id::text OR auth.jwt() ->> 'email' = email)
    WITH CHECK (auth.uid()::text = id::text OR auth.jwt() ->> 'email' = email);

-- Health Profiles: strictly scoped to account owner
CREATE POLICY "profiles_manage_own" ON health_profiles FOR ALL TO authenticated
    USING (auth.uid()::text = user_id::text)
    WITH CHECK (auth.uid()::text = user_id::text);

-- Medical Documents & Biomarkers: strictly scoped to document owner
CREATE POLICY "docs_manage_own" ON medical_documents FOR ALL TO authenticated
    USING (auth.uid()::text = user_id::text)
    WITH CHECK (auth.uid()::text = user_id::text);

CREATE POLICY "biomarkers_manage_own" ON biomarkers FOR ALL TO authenticated
    USING (auth.uid()::text = user_id::text)
    WITH CHECK (auth.uid()::text = user_id::text);

-- Menstrual Cycles & Symptoms: strictly scoped to patient
CREATE POLICY "cycles_manage_own" ON cycle_records FOR ALL TO authenticated
    USING (auth.uid()::text = user_id::text)
    WITH CHECK (auth.uid()::text = user_id::text);

CREATE POLICY "symptoms_manage_own" ON symptom_records FOR ALL TO authenticated
    USING (auth.uid()::text = user_id::text)
    WITH CHECK (auth.uid()::text = user_id::text);

-- Reminders & Completions
CREATE POLICY "reminders_manage_own" ON care_reminders FOR ALL TO authenticated
    USING (auth.uid()::text = user_id::text)
    WITH CHECK (auth.uid()::text = user_id::text);

CREATE POLICY "completions_manage_own" ON reminder_completions FOR ALL TO authenticated
    USING (EXISTS (SELECT 1 FROM care_reminders r WHERE r.id = reminder_id AND auth.uid()::text = r.user_id::text))
    WITH CHECK (EXISTS (SELECT 1 FROM care_reminders r WHERE r.id = reminder_id AND auth.uid()::text = r.user_id::text));

-- AI Conversations & Chat Messages
CREATE POLICY "conversations_manage_own" ON conversations FOR ALL TO authenticated
    USING (auth.uid()::text = user_id::text)
    WITH CHECK (auth.uid()::text = user_id::text);

CREATE POLICY "chat_messages_manage_own" ON chat_messages FOR ALL TO authenticated
    USING (EXISTS (SELECT 1 FROM conversations c WHERE c.id = conversation_id AND auth.uid()::text = c.user_id::text))
    WITH CHECK (EXISTS (SELECT 1 FROM conversations c WHERE c.id = conversation_id AND auth.uid()::text = c.user_id::text));

-- Doctor Consultation Briefs
CREATE POLICY "briefs_manage_own" ON consultation_briefs FOR ALL TO authenticated
    USING (auth.uid()::text = user_id::text)
    WITH CHECK (auth.uid()::text = user_id::text);

-- Meal Plans & Items
CREATE POLICY "meal_plans_manage_own" ON meal_plans FOR ALL TO authenticated
    USING (auth.uid()::text = user_id::text)
    WITH CHECK (auth.uid()::text = user_id::text);

CREATE POLICY "meal_plan_items_manage_own" ON meal_plan_items FOR ALL TO authenticated
    USING (EXISTS (SELECT 1 FROM meal_plans mp WHERE mp.id = meal_plan_id AND auth.uid()::text = mp.user_id::text))
    WITH CHECK (EXISTS (SELECT 1 FROM meal_plans mp WHERE mp.id = meal_plan_id AND auth.uid()::text = mp.user_id::text));

-- Notifications
CREATE POLICY "notifications_manage_own" ON notifications FOR ALL TO authenticated
    USING (auth.uid()::text = user_id::text)
    WITH CHECK (auth.uid()::text = user_id::text);

-- ------------------------------------------------------------------------------
-- 4. Public Nutritional Knowledge Base & Community Forum Policies
-- ------------------------------------------------------------------------------

-- Meal Items: Read-only for all users (public Indian nutritional library)
CREATE POLICY "meal_items_read_all" ON meal_items FOR SELECT TO anon, authenticated
    USING (true);

-- Community Posts: Read active posts; create/update own posts
CREATE POLICY "community_posts_read_active" ON community_posts FOR SELECT TO anon, authenticated
    USING (status = 'active');

CREATE POLICY "community_posts_insert" ON community_posts FOR INSERT TO authenticated
    WITH CHECK (auth.uid()::text = user_id::text OR user_id IS NULL);

CREATE POLICY "community_posts_update_own" ON community_posts FOR UPDATE TO authenticated
    USING (auth.uid()::text = user_id::text)
    WITH CHECK (auth.uid()::text = user_id::text);

-- Community Replies: Read active replies; insert authenticated
CREATE POLICY "community_replies_read_active" ON community_replies FOR SELECT TO anon, authenticated
    USING (status = 'active');

CREATE POLICY "community_replies_insert" ON community_replies FOR INSERT TO authenticated
    WITH CHECK (auth.uid()::text = user_id::text OR user_id IS NULL);

-- Content Reports: anyone can submit a report; only staff/service_role can view
CREATE POLICY "content_reports_insert" ON content_reports FOR INSERT TO anon, authenticated
    WITH CHECK (true);
