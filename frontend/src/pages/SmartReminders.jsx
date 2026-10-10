import React, { useState } from 'react';
import PageHeader from '../components/PageHeader';
import ReminderCard from '../components/ReminderCard';
import Modal from '../components/Modal';
import FormField from '../components/FormField';
import ConfirmDialog from '../components/ConfirmDialog';
import { useNotifications } from '../hooks/useNotifications';

export default function SmartReminders({ reminders, setReminders, language }) {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingReminder, setEditingReminder] = useState(null);
  const [reminderToDelete, setReminderToDelete] = useState(null);
  const [activeTab, setActiveTab] = useState('all'); // all, active, completed

  // Form states
  const [title, setTitle] = useState('');
  const [category, setCategory] = useState('medication');
  const [time, setTime] = useState('08:30 AM');
  const [date, setDate] = useState(new Date().toISOString().split('T')[0]);
  const [frequency, setFrequency] = useState('Daily');
  const [notes, setNotes] = useState('');

  const { permission, isSupported: notifSupported, requestPermission, sendNotification } = useNotifications();
  const isTelugu = language === 'te';

  const handleToggleComplete = (id) => {
    setReminders(
      reminders.map((r) =>
        r.id === id ? { ...r, completed: !r.completed } : r
      )
    );
  };

  const handleSnooze = (id) => {
    setReminders(
      reminders.map((r) => {
        if (r.id === id) {
          return {
            ...r,
            time: `${r.time} (+30m snoozed)`,
            notes: (r.notes ? r.notes + ' • ' : '') + 'Snoozed 30 mins'
          };
        }
        return r;
      })
    );
  };

  const handleOpenAdd = () => {
    setEditingReminder(null);
    setTitle('');
    setCategory('medication');
    setTime('08:30 AM');
    setDate(new Date().toISOString().split('T')[0]);
    setFrequency('Daily');
    setNotes('');
    setIsModalOpen(true);
  };

  const handleOpenEdit = (rem) => {
    setEditingReminder(rem);
    setTitle(rem.title);
    setCategory(rem.category || 'medication');
    setTime(rem.time || '08:30 AM');
    setDate(rem.date || new Date().toISOString().split('T')[0]);
    setFrequency(rem.frequency || 'Daily');
    setNotes(rem.notes || '');
    setIsModalOpen(true);
  };

  const handleSaveReminder = (e) => {
    e.preventDefault();
    if (!title.trim()) return;

    if (editingReminder) {
      setReminders(
        reminders.map((r) =>
          r.id === editingReminder.id
            ? { ...r, title: title.trim(), category, time, date, frequency, notes: notes.trim() }
            : r
        )
      );
    } else {
      const newRem = {
        id: `rem-${Date.now()}`,
        title: title.trim(),
        category,
        time,
        date,
        frequency,
        notes: notes.trim(),
        completed: false
      };
      setReminders([newRem, ...reminders]);

      if (permission === 'granted') {
        sendNotification(`Health Saathi Reminder: ${newRem.title}`, {
          body: `Scheduled for ${newRem.time} (${newRem.frequency})`
        });
      }
    }

    setIsModalOpen(false);
  };

  const confirmDeleteReminder = () => {
    if (reminderToDelete) {
      setReminders(reminders.filter((r) => r.id !== reminderToDelete.id));
      setReminderToDelete(null);
    }
  };

  const filteredReminders = reminders.filter((r) => {
    if (activeTab === 'active') return !r.completed;
    if (activeTab === 'completed') return r.completed;
    return true;
  });

  return (
    <div>
      <PageHeader
        title={isTelugu ? 'స్మార్ట్ కేర్ రిమైండర్లు' : 'Smart Care Reminders'}
        subtitle={isTelugu
          ? 'మీ ఔషధాలు, డాక్టర్ అపాయింట్‌మెంట్లు, మరియు జీవనశైలి అలవాట్లను క్రమబద్ధంగా నిర్వహించండి.'
          : 'Maintain continuity of care for clinician-prescribed medications, upcoming blood tests, hydration, and movement routines.'}
        badge="Care Routines"
        actions={
          <button onClick={handleOpenAdd} className="btn btn-primary">
            + {isTelugu ? 'రిమైండర్ జోడించండి' : 'Add Care Reminder'}
          </button>
        }
      />

      {/* Notification Permission Card */}
      <div style={{
        background: 'var(--bg-card)',
        border: '1px solid var(--border-subtle)',
        borderRadius: 'var(--radius-md)',
        padding: '14px 20px',
        marginBottom: '20px',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        flexWrap: 'wrap',
        gap: '12px'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <span style={{ fontSize: '1.3rem' }}>🔔</span>
          <div>
            <div style={{ fontWeight: 600, fontSize: '0.88rem', color: 'var(--text-primary)' }}>
              Browser Notification Integration
            </div>
            <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
              Status: <strong>{permission}</strong> • {
                permission === 'granted' ? 'Desktop alerts enabled for care tasks' :
                permission === 'denied' ? 'Permission denied in browser settings' :
                'Enable browser notifications to receive timely habit reminders'
              }
            </div>
          </div>
        </div>

        {permission !== 'granted' && notifSupported && (
          <button onClick={requestPermission} className="btn btn-outline btn-sm">
            Enable Notifications
          </button>
        )}
      </div>

      {/* Filter Tabs */}
      <div style={{ display: 'flex', gap: '8px', marginBottom: '20px' }}>
        {[
          { id: 'all', label: `All (${reminders.length})` },
          { id: 'active', label: `Pending (${reminders.filter(r => !r.completed).length})` },
          { id: 'completed', label: `Completed (${reminders.filter(r => r.completed).length})` }
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`btn btn-sm ${activeTab === tab.id ? 'btn-primary' : 'btn-outline'}`}
            style={{ borderRadius: 'var(--radius-full)' }}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Reminder Cards Feed */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
        {filteredReminders.length === 0 ? (
          <div className="card" style={{ textAlign: 'center', padding: '40px', color: 'var(--text-muted)' }}>
            No reminders in this view.
          </div>
        ) : (
          filteredReminders.map((rem) => (
            <div key={rem.id} style={{ position: 'relative' }}>
              <ReminderCard
                reminder={rem}
                onToggleComplete={handleToggleComplete}
                onDelete={() => setReminderToDelete(rem)}
              />
              <div style={{ position: 'absolute', top: '16px', right: '55px', display: 'flex', gap: '6px' }}>
                {!rem.completed && (
                  <button
                    onClick={() => handleSnooze(rem.id)}
                    className="btn btn-ghost btn-sm"
                    title="Snooze 30 mins"
                    style={{ fontSize: '0.72rem', padding: '2px 6px', color: 'var(--primary-700)' }}
                  >
                    ⏰ Snooze
                  </button>
                )}
                <button
                  onClick={() => handleOpenEdit(rem)}
                  className="btn btn-ghost btn-sm"
                  title="Edit reminder"
                  style={{ fontSize: '0.8rem', padding: '2px 6px' }}
                >
                  ✏️
                </button>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Add / Edit Reminder Modal */}
      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title={editingReminder ? '✏️ Edit Care Reminder' : '⏰ Add Care Reminder'}
        maxWidth="500px"
      >
        <form onSubmit={handleSaveReminder}>
          <FormField
            label="Reminder Title / Care Routine"
            id="rem-title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="e.g. Myo-Inositol Sachet, Metformin, 20m Post-Meal Walk"
            required
          />

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px', marginBottom: '16px' }}>
            <div>
              <label style={{ display: 'block', fontSize: '0.84rem', fontWeight: 600, marginBottom: '6px' }}>
                Category
              </label>
              <select
                value={category}
                onChange={(e) => setCategory(e.target.value)}
                style={{ width: '100%' }}
              >
                <option value="medication">Prescribed Medication</option>
                <option value="supplement">Supplement (Inositol, Vit D)</option>
                <option value="lifestyle">Lifestyle / Walking Habit</option>
                <option value="hydration">Hydration / Water</option>
                <option value="appointment">Doctor / Lab Appointment</option>
              </select>
            </div>

            <div>
              <label style={{ display: 'block', fontSize: '0.84rem', fontWeight: 600, marginBottom: '6px' }}>
                Time of Day
              </label>
              <input
                type="text"
                value={time}
                onChange={(e) => setTime(e.target.value)}
                placeholder="08:30 AM"
                style={{ width: '100%' }}
              />
            </div>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px', marginBottom: '16px' }}>
            <FormField
              label="Recurrence"
              id="rem-freq"
              value={frequency}
              onChange={(e) => setFrequency(e.target.value)}
              placeholder="Daily, Weekly"
            />
            <FormField
              label="Start Date"
              id="rem-date"
              type="date"
              value={date}
              onChange={(e) => setDate(e.target.value)}
            />
          </div>

          <FormField
            label="Notes / Instructions"
            id="rem-notes"
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
            placeholder="e.g. Take with warm water after dinner"
          />

          <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '10px', marginTop: '20px' }}>
            <button type="button" onClick={() => setIsModalOpen(false)} className="btn btn-outline btn-sm">
              Cancel
            </button>
            <button type="submit" className="btn btn-primary btn-sm">
              {editingReminder ? 'Save Changes' : 'Create Reminder'}
            </button>
          </div>
        </form>
      </Modal>

      {/* Delete Confirmation */}
      <ConfirmDialog
        isOpen={Boolean(reminderToDelete)}
        title="Remove Care Reminder"
        message={`Are you sure you want to remove the reminder "${reminderToDelete?.title}"?`}
        confirmLabel="Remove"
        isDestructive={true}
        onConfirm={confirmDeleteReminder}
        onCancel={() => setReminderToDelete(null)}
      />
    </div>
  );
}
