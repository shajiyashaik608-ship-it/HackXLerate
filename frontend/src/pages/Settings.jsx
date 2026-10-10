import React, { useState, useEffect } from 'react';
import PageHeader from '../components/PageHeader';
import ConfirmDialog from '../components/ConfirmDialog';
import { storageService, STORAGE_KEYS } from '../services/storageService';

export default function Settings({
  language,
  setLanguage,
  onResetAllData,
  onClearChat
}) {
  const [notificationSounds, setNotificationSounds] = useState(true);
  const [storageUsage, setStorageUsage] = useState({ kb: '0.00', label: '0 KB' });
  const [confirmModal, setConfirmModal] = useState({ isOpen: false, type: '', title: '', message: '' });
  const [feedbackMsg, setFeedbackMsg] = useState('');

  const isTelugu = language === 'te';

  useEffect(() => {
    updateStorageSize();
  }, []);

  const updateStorageSize = () => {
    setStorageUsage(storageService.getStorageUsage());
  };

  const handleExportJSON = () => {
    const success = storageService.exportHealthData();
    if (success) {
      setFeedbackMsg('✅ Health data exported successfully to JSON file.');
      setTimeout(() => setFeedbackMsg(''), 3000);
    }
  };

  const handleImportJSON = (e) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (event) => {
      const content = event.target?.result;
      const res = storageService.importHealthData(content);
      if (res.success) {
        setFeedbackMsg('✅ Backup restored. Please refresh page to load imported records.');
        updateStorageSize();
      } else {
        alert(`Import failed: ${res.error}`);
      }
    };
    reader.readAsText(file);
  };

  const executeConfirmAction = () => {
    if (confirmModal.type === 'reset-all') {
      onResetAllData();
      setFeedbackMsg('✓ All demo data has been restored to default values.');
    } else if (confirmModal.type === 'clear-chat') {
      onClearChat();
      setFeedbackMsg('✓ Chat history cleared.');
    } else if (confirmModal.type === 'clear-cycle') {
      storageService.clearCategory(STORAGE_KEYS.CYCLE_LOGS);
      setFeedbackMsg('✓ Menstrual cycle logs cleared.');
    } else if (confirmModal.type === 'clear-reports') {
      storageService.clearCategory(STORAGE_KEYS.REPORTS);
      setFeedbackMsg('✓ Stored medical reports cleared.');
    }

    updateStorageSize();
    setConfirmModal({ isOpen: false, type: '', title: '', message: '' });
    setTimeout(() => setFeedbackMsg(''), 3500);
  };

  return (
    <div style={{ maxWidth: '820px', margin: '0 auto' }}>
      <PageHeader
        title={isTelugu ? 'అప్లికేషన్ సెట్టింగ్స్' : 'Application Settings & Privacy'}
        subtitle={isTelugu
          ? 'భాష, డేటా నిర్వహణ మరియు గోప్యతా విధానాలను ఇక్కడ నియంత్రించండి.'
          : 'Manage linguistic preferences, browser local storage telemetry, and demo privacy settings.'}
        badge="Privacy Controls"
      />

      {feedbackMsg && (
        <div style={{
          background: 'var(--accent-green-light)',
          color: '#166534',
          padding: '12px 18px',
          borderRadius: 'var(--radius-md)',
          marginBottom: '20px',
          fontWeight: 600,
          border: '1px solid var(--accent-green)'
        }}>
          {feedbackMsg}
        </div>
      )}

      {/* Language Settings */}
      <div className="card" style={{ marginBottom: '20px' }}>
        <h3 style={{ fontSize: '1.15rem', color: 'var(--text-primary)', marginBottom: '14px' }}>
          🌐 Language & Localization
        </h3>
        <div className="form-group">
          <label className="form-label" style={{ display: 'block', fontSize: '0.84rem', fontWeight: 600, marginBottom: '6px' }}>
            Primary UI & Assistant Language
          </label>
          <div style={{ display: 'flex', gap: '10px' }}>
            <button
              onClick={() => setLanguage('en')}
              className={`btn ${language === 'en' ? 'btn-primary' : 'btn-outline'}`}
            >
              English
            </button>
            <button
              onClick={() => setLanguage('te')}
              className={`btn ${language === 'te' ? 'btn-primary' : 'btn-outline'}`}
            >
              తెలుగు (Telugu - Voice Ready)
            </button>
          </div>
          <span className="form-hint" style={{ display: 'block', fontSize: '0.78rem', color: 'var(--text-muted)', marginTop: '6px' }}>
            Telugu enables bilingual Telugu voice assistance (STT/TTS) and regional nutrition recommendations.
          </span>
        </div>
      </div>

      {/* Privacy & Storage Telemetry */}
      <div className="card" style={{ marginBottom: '20px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '14px' }}>
          <h3 style={{ fontSize: '1.15rem', color: 'var(--text-primary)', margin: 0 }}>
            🔒 Privacy & Storage Architecture
          </h3>
          <span className="badge badge-primary">Used: {storageUsage.label}</span>
        </div>
        <p style={{ fontSize: '0.86rem', color: 'var(--text-secondary)', lineHeight: 1.6, marginBottom: '12px' }}>
          PCOS Saathi stores all demo inputs (cycle dates, symptoms, uploaded report names, reminder lists) inside your browser's local sandbox (<code>localStorage</code>).
        </p>
        <div style={{
          background: 'var(--bg-subtle)',
          padding: '12px 16px',
          borderRadius: '8px',
          fontSize: '0.82rem',
          color: 'var(--text-muted)',
          lineHeight: 1.5,
          marginBottom: '16px'
        }}>
          ⚠️ <strong>Security Transparency:</strong> Browser localStorage is strictly client-side for hackathon demonstration. It does not provide medical-grade HIPAA/GDPR encryption. No private records leave your browser.
        </div>

        {/* Export and Import Actions */}
        <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
          <button onClick={handleExportJSON} className="btn btn-outline btn-sm">
            💾 Export Records to JSON File
          </button>
          <label className="btn btn-outline btn-sm" style={{ cursor: 'pointer', margin: 0 }}>
            📥 Import Backup JSON
            <input
              type="file"
              accept=".json"
              onChange={handleImportJSON}
              style={{ display: 'none' }}
            />
          </label>
        </div>
      </div>

      {/* Granular & Destructive Demo Controls */}
      <div className="card" style={{ borderColor: 'var(--coral-500)' }}>
        <h3 style={{ fontSize: '1.15rem', color: 'var(--coral-700)', marginBottom: '14px' }}>
          ⚙️ Demo Data Cleanup & Reset
        </h3>
        <p style={{ fontSize: '0.84rem', color: 'var(--text-muted)', marginBottom: '14px' }}>
          Reset specific records or restore default synthetic hackathon demonstration data:
        </p>

        <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
          <button
            onClick={() => setConfirmModal({
              isOpen: true,
              type: 'clear-chat',
              title: 'Clear Chat History',
              message: 'Are you sure you want to clear your AI Assistant conversation logs?'
            })}
            className="btn btn-outline btn-sm"
          >
            Clear Chat Logs
          </button>
          <button
            onClick={() => setConfirmModal({
              isOpen: true,
              type: 'clear-cycle',
              title: 'Clear Menstrual Cycle Logs',
              message: 'Are you sure you want to delete all recorded menstrual cycle entries?'
            })}
            className="btn btn-outline btn-sm"
          >
            Clear Cycle Records
          </button>
          <button
            onClick={() => setConfirmModal({
              isOpen: true,
              type: 'clear-reports',
              title: 'Clear Stored Reports',
              message: 'Are you sure you want to delete all uploaded medical reports?'
            })}
            className="btn btn-outline btn-sm"
          >
            Clear Reports
          </button>
          <button
            onClick={() => setConfirmModal({
              isOpen: true,
              type: 'reset-all',
              title: 'Restore Default Demo Data',
              message: 'This will reset all records (cycle logs, uploaded reports, custom reminders) and restore synthetic demo profiles. Proceed?'
            })}
            className="btn btn-coral btn-sm"
          >
            ⚠️ Reset All to Demo Defaults
          </button>
        </div>
      </div>

      {/* Confirmation Dialog */}
      <ConfirmDialog
        isOpen={confirmModal.isOpen}
        title={confirmModal.title}
        message={confirmModal.message}
        confirmLabel="Proceed"
        isDestructive={true}
        onConfirm={executeConfirmAction}
        onCancel={() => setConfirmModal({ isOpen: false, type: '', title: '', message: '' })}
      />
    </div>
  );
}
