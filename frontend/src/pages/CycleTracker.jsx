import React, { useState } from 'react';
import PageHeader from '../components/PageHeader';
import Modal from '../components/Modal';
import CycleSummary from '../features/cycle/CycleSummary';
import CycleCalendar from '../features/cycle/CycleCalendar';
import CycleLogForm from '../features/cycle/CycleLogForm';
import ConfirmDialog from '../components/ConfirmDialog';
import { formatDisplayDate } from '../utils/dateUtils';

export default function CycleTracker({ cycleLogs, setCycleLogs, profile, language }) {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingLog, setEditingLog] = useState(null);
  const [logToDelete, setLogToDelete] = useState(null);

  const isTelugu = language === 'te';

  const handleSaveLog = (newEntry) => {
    if (editingLog) {
      setCycleLogs(cycleLogs.map((c) => (c.id === newEntry.id ? newEntry : c)));
      setEditingLog(null);
    } else {
      setCycleLogs([newEntry, ...cycleLogs]);
    }
    setIsModalOpen(false);
  };

  const handleEditClick = (log) => {
    setEditingLog(log);
    setIsModalOpen(true);
  };

  const confirmDeleteLog = () => {
    if (logToDelete) {
      setCycleLogs(cycleLogs.filter((c) => c.id !== logToDelete.id));
      setLogToDelete(null);
    }
  };

  return (
    <div>
      <PageHeader
        title={isTelugu ? 'పీరియడ్ & లక్షణాల ట్రాకర్' : 'Menstrual Cycle & Symptom Tracker'}
        subtitle={isTelugu
          ? 'PCOS సైకిల్స్ లోని సహజమైన మార్పులను గమనిస్తూ, డాక్టర్ సంప్రదింపులకు అవసరమైన రికార్డును సిద్ధం చేసుకోండి.'
          : 'Track flow patterns, cycle intervals, and daily symptoms. Models natural PCOS variance rather than rigid calendar rules.'}
        badge="Variance Aware"
        actions={
          <button
            onClick={() => { setEditingLog(null); setIsModalOpen(true); }}
            className="btn btn-coral"
          >
            🌸 {isTelugu ? '+ పీరియడ్ నమోదు చేయండి' : '+ Log Period Cycle'}
          </button>
        }
      />

      {/* Uncertainty & Medical Transparency Banner */}
      <div style={{
        background: 'var(--primary-50)',
        border: '1px solid var(--primary-200)',
        borderRadius: 'var(--radius-md)',
        padding: '12px 18px',
        marginBottom: '20px',
        fontSize: '0.82rem',
        color: 'var(--primary-900)',
        lineHeight: 1.5,
        display: 'flex',
        alignItems: 'center',
        gap: '10px'
      }}>
        <span style={{ fontSize: '1.2rem' }}>ℹ️</span>
        <span>
          <strong>PCOS Variance Principle:</strong> Unlike standard 28-day assumptions, PCOS menstrual intervals naturally vary by ±4 to 6 days due to delayed follicular maturation. All future dates are displayed as estimated windows rather than guaranteed arrival dates.
        </span>
      </div>

      {/* Cycle Summary Metrics */}
      <CycleSummary cycleLogs={cycleLogs} avgCycleLength={profile.cycleLength || 33} />

      {/* Grid: Calendar on Left, History on Right */}
      <div className="grid-2">
        <CycleCalendar cycleLogs={cycleLogs} />

        {/* History List */}
        <div className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '14px' }}>
            <h3 style={{ fontSize: '1.15rem', color: 'var(--text-primary)', margin: 0 }}>
              📜 Logged Cycle History ({cycleLogs.length})
            </h3>
            <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
              Click ✏️ to edit or 🗑️ to delete
            </span>
          </div>

          {cycleLogs.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '30px 0', color: 'var(--text-muted)', fontSize: '0.86rem' }}>
              No menstrual logs recorded yet. Click "+ Log Period Cycle" above.
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
              {cycleLogs.map((log) => (
                <div
                  key={log.id}
                  style={{
                    background: 'var(--bg-subtle)',
                    borderRadius: 'var(--radius-md)',
                    padding: '14px',
                    border: '1px solid var(--border-subtle)',
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'flex-start'
                  }}
                >
                  <div>
                    <div style={{ fontWeight: 700, fontSize: '0.94rem', color: 'var(--text-primary)' }}>
                      Started on {formatDisplayDate(log.startDate)}
                    </div>
                    <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginTop: '2px' }}>
                      Flow: <strong>{log.flow}</strong> • Duration: {log.durationDays} days
                    </div>
                    {log.symptoms?.length > 0 && (
                      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '4px', marginTop: '6px' }}>
                        {log.symptoms.map((s, idx) => (
                          <span key={idx} className="badge badge-coral" style={{ fontSize: '0.68rem', padding: '1px 6px' }}>
                            {s}
                          </span>
                        ))}
                      </div>
                    )}
                    {log.notes && (
                      <div style={{ fontSize: '0.78rem', color: 'var(--text-secondary)', marginTop: '6px', fontStyle: 'italic' }}>
                        "{log.notes}"
                      </div>
                    )}
                  </div>

                  <div style={{ display: 'flex', gap: '6px' }}>
                    <button
                      onClick={() => handleEditClick(log)}
                      className="btn btn-ghost btn-sm"
                      title="Edit cycle entry"
                      style={{ padding: '4px 6px', fontSize: '0.9rem' }}
                    >
                      ✏️
                    </button>
                    <button
                      onClick={() => setLogToDelete(log)}
                      className="btn btn-ghost btn-sm"
                      title="Delete log"
                      style={{ color: 'var(--coral-600)', padding: '4px 6px', fontSize: '0.9rem' }}
                    >
                      🗑️
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Log Cycle Modal */}
      <Modal
        isOpen={isModalOpen}
        onClose={() => { setIsModalOpen(false); setEditingLog(null); }}
        title={editingLog ? '✏️ Edit Menstrual Cycle Record' : '🌸 Log Menstrual Cycle'}
        maxWidth="520px"
      >
        <CycleLogForm
          initialData={editingLog}
          onSave={handleSaveLog}
          onCancel={() => { setIsModalOpen(false); setEditingLog(null); }}
        />
      </Modal>

      {/* Delete Confirmation */}
      <ConfirmDialog
        isOpen={Boolean(logToDelete)}
        title="Delete Cycle Entry"
        message={`Are you sure you want to delete the cycle record starting on ${logToDelete?.startDate ? formatDisplayDate(logToDelete.startDate) : ''}?`}
        confirmLabel="Delete Record"
        isDestructive={true}
        onConfirm={confirmDeleteLog}
        onCancel={() => setLogToDelete(null)}
      />
    </div>
  );
}
