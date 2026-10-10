import React, { useState } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';

// Layout & Navigation Components
import Sidebar from './components/Sidebar';
import Navbar from './components/Navbar';
import MobileNavigation from './components/MobileNavigation';
import SafetyBanner from './components/SafetyBanner';
import AuthModal from './components/AuthModal';
import OnboardingModal from './components/OnboardingModal';
import Toast from './components/Toast';

// Custom Hooks
import { useLocalStorage } from './hooks/useLocalStorage';

// Sample Data
import { SAMPLE_REPORTS } from './data/sampleReports';
import { SAMPLE_REMINDERS } from './data/sampleReminders';
import { SAMPLE_POSTS } from './data/samplePosts';

// Pages
import Welcome from './pages/Welcome';
import Dashboard from './pages/Dashboard';
import HealthProfile from './pages/HealthProfile';
import HealthAssistant from './pages/HealthAssistant';
import CycleTracker from './pages/CycleTracker';
import FoodCompanion from './pages/FoodCompanion';
import MedicalReports from './pages/MedicalReports';
import DoctorPreparation from './pages/DoctorPreparation';
import SmartReminders from './pages/SmartReminders';
import Community from './pages/Community';
import Settings from './pages/Settings';
import NotFound from './pages/NotFound';

// Styles
import './styles/global.css';
import './styles/components.css';
import './styles/responsive.css';

export default function App() {
  // Persistent State via localStorage
  const [language, setLanguage] = useLocalStorage('pcos_saathi_lang', 'en');

  const [profile, setProfile] = useLocalStorage('pcos_saathi_profile', {
    name: 'Priya Sharma',
    age: 24,
    language: 'en',
    dietType: 'vegetarian',
    allergies: 'None',
    cycleLength: 33,
    periodDuration: 4,
    wellnessGoals: 'Manage insulin resistance and establish predictable menstrual cycles.'
  });

  const [cycleLogs, setCycleLogs] = useLocalStorage('pcos_saathi_cycle_logs', [
    {
      id: 1,
      startDate: '2026-09-25',
      durationDays: 4,
      flow: 'medium',
      symptoms: ['cramps', 'fatigue'],
      notes: 'Cycle started after 38-day interval.'
    },
    {
      id: 2,
      startDate: '2026-08-18',
      durationDays: 4,
      flow: 'medium',
      symptoms: ['bloating'],
      notes: 'Normal flow, mild afternoon tiredness.'
    }
  ]);

  const [reports, setReports] = useLocalStorage('pcos_saathi_reports', SAMPLE_REPORTS);
  const [reminders, setReminders] = useLocalStorage('pcos_saathi_reminders', SAMPLE_REMINDERS);
  const [posts, setPosts] = useLocalStorage('pcos_saathi_posts', SAMPLE_POSTS);

  const [dailyPlan, setDailyPlan] = useLocalStorage('pcos_saathi_meal_plan', {
    breakfast: {
      id: 'meal-1',
      name: 'Moong Dal Pesarattu with Ginger Chutney',
      category: 'breakfast',
      image: '🌱',
      proteinSources: '14g plant protein',
      approxCalories: '260 kcal',
      balancedExplanation: 'Low glycemic index releases glucose slowly into the bloodstream.'
    },
    lunch: null,
    dinner: null
  });

  const [notifications, setNotifications] = useLocalStorage('pcos_saathi_notifs', [
    {
      id: 1,
      icon: '🌸',
      title: 'Estimated Cycle Window',
      message: 'Estimated next period window approaching in ~2 weeks (Oct 28 - Nov 03).',
      time: 'Today',
      read: false
    },
    {
      id: 2,
      icon: '⏰',
      title: 'Medication Routine',
      message: 'Myo-Inositol sachet scheduled for 08:30 AM.',
      time: 'Today',
      read: false
    },
    {
      id: 3,
      icon: '📄',
      title: 'Lab Report Flag',
      message: 'TSH biomarker (4.85 mIU/L) flagged for Doctor Consultation Brief review.',
      time: 'Yesterday',
      read: true
    }
  ]);

  const [chatHistory, setChatHistory] = useLocalStorage('pcos_saathi_chat_history', [
    {
      id: 1,
      sender: 'assistant',
      text: language === 'te'
        ? "నమస్తే! నేను మీ పిసిఒఎస్ సాథి AI అసిస్టెంట్. పీరియడ్స్, ఆహారపు అలవాట్లు లేదా రిపోర్టుల గురించి ఏదైనా అడగండి."
        : "Hello! I am your PCOS Saathi companion. Ask me any health-education questions about cycle rhythms, Indian meals, or doctor visit preparation.",
      sources: ["WHO Guidelines", "FOGSI Indian Clinical Consensus"],
      disclaimer: "Educational simulation only. Consult a doctor for medical diagnoses.",
      timestamp: 'Just now'
    }
  ]);

  // Modal & Navigation States
  const [mobileNavOpen, setMobileNavOpen] = useState(false);
  const [authModalOpen, setAuthModalOpen] = useState(false);
  const [onboardingModalOpen, setOnboardingModalOpen] = useState(false);
  const [toast, setToast] = useState({ isOpen: false, message: '', type: 'info' });

  const showToast = (message, type = 'info') => {
    setToast({ isOpen: true, message, type });
  };

  // Persona & Auth Selection
  const handleSelectPersona = (selectedPersona) => {
    setProfile(selectedPersona);
    showToast(`Active persona switched to ${selectedPersona.name}`, 'success');
  };

  const handleLogout = () => {
    setProfile({
      name: 'Guest User',
      age: 25,
      language: 'en',
      dietType: 'all',
      cycleLength: 30,
      periodDuration: 4,
      wellnessGoals: 'Evaluating Health Saathi application.'
    });
    setAuthModalOpen(false);
    showToast('Signed out of demo persona', 'info');
  };

  // Notification actions
  const handleMarkNotifRead = (id) => {
    setNotifications(
      notifications.map((n) => (n.id === id ? { ...n, read: true } : n))
    );
  };

  const handleClearNotifs = () => {
    setNotifications([]);
    showToast('All notifications cleared', 'info');
  };

  // Reset entire state to demo defaults
  const handleResetAllData = () => {
    window.localStorage.clear();
    setProfile({
      name: 'Priya Sharma',
      age: 24,
      language: 'en',
      dietType: 'vegetarian',
      allergies: 'None',
      cycleLength: 33,
      periodDuration: 4,
      wellnessGoals: 'Manage insulin resistance and establish predictable menstrual cycles.'
    });
    setReports(SAMPLE_REPORTS);
    setReminders(SAMPLE_REMINDERS);
    setPosts(SAMPLE_POSTS);
    setDailyPlan({ breakfast: null, lunch: null, dinner: null });
    setChatHistory([
      {
        id: 1,
        sender: 'assistant',
        text: "Hello! I am your PCOS Saathi companion. Ask me any health-education questions.",
        sources: ["WHO Guidelines"],
        disclaimer: "Educational simulation only.",
        timestamp: 'Just now'
      }
    ]);
    showToast('All records restored to demo defaults', 'success');
  };

  return (
    <BrowserRouter>
      <div className="app-layout">
        {/* Persistent Left Sidebar (Desktop) */}
        <Sidebar
          language={language}
          profile={profile}
          onOpenAuth={() => setAuthModalOpen(true)}
        />

        {/* Main Application Area */}
        <div className="main-wrapper">
          {/* Top Medical Ethics Safety Notice */}
          <SafetyBanner language={language} />

          {/* Top Header Navbar */}
          <Navbar
            language={language}
            setLanguage={setLanguage}
            profile={profile}
            notifications={notifications}
            onMarkNotificationAsRead={handleMarkNotifRead}
            onClearNotifications={handleClearNotifs}
            onToggleMobileNav={() => setMobileNavOpen(!mobileNavOpen)}
            onOpenAuth={() => setAuthModalOpen(true)}
          />

          {/* Content Pages */}
          <main className="content-area">
            <Routes>
              <Route path="/" element={<Navigate to="/welcome" replace />} />
              <Route
                path="/welcome"
                element={
                  <Welcome
                    language={language}
                    onStartOnboarding={() => setOnboardingModalOpen(true)}
                    onOpenAuth={() => setAuthModalOpen(true)}
                  />
                }
              />
              <Route
                path="/dashboard"
                element={
                  <Dashboard
                    profile={profile}
                    cycleLogs={cycleLogs}
                    reminders={reminders}
                    reports={reports}
                    dailyPlan={dailyPlan}
                    language={language}
                  />
                }
              />
              <Route
                path="/profile"
                element={
                  <HealthProfile
                    profile={profile}
                    setProfile={setProfile}
                    language={language}
                    setLanguage={setLanguage}
                  />
                }
              />
              <Route
                path="/assistant"
                element={
                  <HealthAssistant
                    language={language}
                    setLanguage={setLanguage}
                    chatHistory={chatHistory}
                    setChatHistory={setChatHistory}
                  />
                }
              />
              <Route
                path="/cycle"
                element={
                  <CycleTracker
                    cycleLogs={cycleLogs}
                    setCycleLogs={setCycleLogs}
                    profile={profile}
                    language={language}
                  />
                }
              />
              <Route
                path="/food"
                element={
                  <FoodCompanion
                    dailyPlan={dailyPlan}
                    setDailyPlan={setDailyPlan}
                    language={language}
                  />
                }
              />
              <Route
                path="/reports"
                element={
                  <MedicalReports
                    reports={reports}
                    setReports={setReports}
                    language={language}
                  />
                }
              />
              <Route
                path="/doctor-prep"
                element={
                  <DoctorPreparation
                    profile={profile}
                    cycleLogs={cycleLogs}
                    reports={reports}
                    reminders={reminders}
                    language={language}
                  />
                }
              />
              <Route
                path="/reminders"
                element={
                  <SmartReminders
                    reminders={reminders}
                    setReminders={setReminders}
                    language={language}
                  />
                }
              />
              <Route
                path="/community"
                element={
                  <Community
                    posts={posts}
                    setPosts={setPosts}
                    language={language}
                  />
                }
              />
              <Route
                path="/settings"
                element={
                  <Settings
                    language={language}
                    setLanguage={setLanguage}
                    onResetAllData={handleResetAllData}
                    onClearChat={() => { setChatHistory([]); showToast('Chat history cleared', 'info'); }}
                  />
                }
              />
              <Route path="*" element={<NotFound />} />
            </Routes>
          </main>

          {/* Touch-Friendly Bottom Navigation (Mobile screens <= 768px) */}
          <MobileNavigation language={language} />
        </div>
      </div>

      {/* Simulated Authentication & Persona Switcher Modal */}
      <AuthModal
        isOpen={authModalOpen}
        onClose={() => setAuthModalOpen(false)}
        currentUser={profile}
        onSelectPersona={handleSelectPersona}
        onLogout={handleLogout}
      />

      {/* First-Time Onboarding Experience Modal */}
      <OnboardingModal
        isOpen={onboardingModalOpen}
        onClose={() => setOnboardingModalOpen(false)}
        language={language}
        setLanguage={setLanguage}
        profile={profile}
        setProfile={setProfile}
        onComplete={() => showToast('Onboarding completed! Welcome to Health Saathi.', 'success')}
      />

      {/* Global Accessible Feedback Toast */}
      <Toast
        isOpen={toast.isOpen}
        message={toast.message}
        type={toast.type}
        onClose={() => setToast({ ...toast, isOpen: false })}
      />
    </BrowserRouter>
  );
}
