import React from 'react';
import { useNavigate } from 'react-router-dom';
import StatCard from '../components/StatCard';
import { formatDisplayDate, estimateNextPeriod, calculateCyclePhase } from '../utils/dateUtils';

export default function Dashboard({
  profile,
  cycleLogs,
  reminders,
  reports,
  dailyPlan,
  language
}) {
  const navigate = useNavigate();
  const isTelugu = language === 'te';

  const latestCycle = cycleLogs.length > 0 ? cycleLogs[0] : null;
  const cycleEstimate = latestCycle ? estimateNextPeriod(latestCycle.startDate, profile.cycleLength || 33) : null;
  const phaseInfo = latestCycle ? calculateCyclePhase(latestCycle.startDate, profile.cycleLength || 33) : null;
  
  const totalReminders = reminders.length;
  const completedReminders = reminders.filter((r) => r.completed).length;
  const reminderPercent = totalReminders > 0 ? Math.round((completedReminders / totalReminders) * 100) : 0;
  const todayReminders = reminders.filter((r) => !r.completed);

  // Cycle interval data for visual chart
  const cycleIntervalHistory = [
    { label: 'May Cycle', days: 36 },
    { label: 'Jul Cycle', days: 42 },
    { label: 'Aug Cycle', days: 38 },
    { label: 'Sep Cycle', days: cycleLogs[0]?.durationDays ? 34 : 33 }
  ];

  return (
    <div>
      {/* Welcome Banner */}
      <div style={{
        background: 'linear-gradient(135deg, var(--primary-700) 0%, var(--primary-900) 100%)',
        borderRadius: 'var(--radius-xl)',
        padding: '30px 36px',
        color: '#ffffff',
        marginBottom: '26px',
        boxShadow: '0 10px 25px -5px rgba(15, 118, 110, 0.25)',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        flexWrap: 'wrap',
        gap: '20px'
      }}>
        <div style={{ maxWidth: '680px' }}>
          <div style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '8px',
            background: 'rgba(255, 255, 255, 0.2)',
            padding: '4px 12px',
            borderRadius: 'var(--radius-full)',
            fontSize: '0.78rem',
            fontWeight: 600,
            marginBottom: '10px'
          }}>
            <span>🌿</span>
            <span>{isTelugu ? 'రోజువారీ సంరక్షణ మార్గదర్శి' : 'Daily PCOS Health Overview'}</span>
            <span style={{ opacity: 0.8 }}>• Demo Sandbox</span>
          </div>
          <h1 style={{ fontSize: '1.95rem', color: '#ffffff', marginBottom: '8px', lineHeight: 1.2 }}>
            {isTelugu
              ? `నమస్తే ${profile.name || 'ప్రియ'}, ఈరోజు మీ ఆరోగ్యం ఎలా ఉంది?`
              : `Good morning, ${profile.name || 'Priya'}! Let's care for your health today.`}
          </h1>
          <p style={{ color: 'var(--primary-100)', fontSize: '0.92rem', lineHeight: '1.6' }}>
            {isTelugu
              ? 'మీ రక్త పరీక్షలు, ఆహార ప్రణాళిక మరియు పీరియడ్ సైకిల్ వివరాలను ఒకే చోట చూసుకోండి.'
              : 'Consistent daily micro-habits support long-term hormonal balance: adequate hydration, protein-dense Indian meals, and gentle movement.'}
          </p>
        </div>

        <div style={{ display: 'flex', gap: '10px' }}>
          <button
            onClick={() => navigate('/assistant')}
            className="btn btn-coral"
            style={{ borderRadius: 'var(--radius-full)', padding: '12px 22px' }}
          >
            <span>🎙️</span>
            <span>{isTelugu ? 'AI సాథిని అడగండి' : 'Ask PCOS Saathi'}</span>
          </button>
        </div>
      </div>

      {/* Snapshot Cards Grid */}
      <div className="grid-3" style={{ marginBottom: '26px' }}>
        {/* Next Period Estimate */}
        <StatCard
          icon="🌸"
          title={isTelugu ? 'తదుపరి పీరియడ్ అంచనా' : 'Next Period Window'}
          value={cycleEstimate ? cycleEstimate.windowRange : 'Log cycle'}
          subtitle={phaseInfo ? `Day ${phaseInfo.dayNumber} • ${phaseInfo.phaseName}` : 'Add your latest cycle'}
          badge={cycleEstimate ? 'Estimated' : 'Needs Data'}
          badgeVariant="warning"
          footerNote="±4 to 6 days natural PCOS variance expected"
          onClick={() => navigate('/cycle')}
        />

        {/* Today's Care Reminders */}
        <StatCard
          icon="⏰"
          title={isTelugu ? 'నేటి కేర్ రిమైండర్లు' : "Today's Care Tasks"}
          value={`${completedReminders} of ${totalReminders} Done`}
          subtitle={todayReminders.length > 0 ? `${todayReminders[0].title}` : 'All routines completed!'}
          badge={reminderPercent === 100 ? 'All Clear' : `${reminderPercent}% Completed`}
          badgeVariant={reminderPercent === 100 ? 'success' : 'primary'}
          footerNote="Medications & lifestyle micro-habits"
          onClick={() => navigate('/reminders')}
        />

        {/* Latest Medical Report Flag */}
        <StatCard
          icon="📄"
          title={isTelugu ? 'ఇటీవలి ల్యాబ్ రిపోర్ట్' : 'Latest Lab Finding'}
          value={reports.length > 0 ? 'TSH 4.85 mIU/L' : 'No records yet'}
          subtitle={reports.length > 0 ? 'Slightly elevated (Thyroid)' : 'Upload blood test'}
          badge={reports.length > 0 ? 'Review Needed' : 'Empty'}
          badgeVariant={reports.length > 0 ? 'coral' : 'secondary'}
          footerNote="Added to Doctor Consultation Brief"
          onClick={() => navigate('/reports')}
        />
      </div>

      {/* Daily Progress & Cycle Trend Section */}
      <div className="grid-2" style={{ marginBottom: '28px' }}>
        {/* Care Routine Progress */}
        <div className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '14px' }}>
            <h3 style={{ fontSize: '1.08rem', color: 'var(--text-primary)', margin: 0 }}>
              🎯 Today's Care Adherence
            </h3>
            <span className="badge badge-primary">{reminderPercent}% Complete</span>
          </div>

          <div style={{ height: '10px', background: 'var(--bg-subtle)', borderRadius: '5px', overflow: 'hidden', marginBottom: '14px' }}>
            <div
              style={{
                width: `${reminderPercent}%`,
                height: '100%',
                background: 'linear-gradient(90deg, var(--primary-600), var(--primary-700))',
                borderRadius: '5px',
                transition: 'width 0.4s ease'
              }}
            />
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            {reminders.slice(0, 3).map((r) => (
              <div
                key={r.id}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  padding: '8px 12px',
                  borderRadius: 'var(--radius-sm)',
                  background: r.completed ? 'var(--bg-subtle)' : '#ffffff',
                  border: '1px solid var(--border-subtle)'
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <span style={{ fontSize: '0.9rem' }}>{r.completed ? '✅' : '⏳'}</span>
                  <span style={{ fontSize: '0.84rem', textDecoration: r.completed ? 'line-through' : 'none', color: r.completed ? 'var(--text-muted)' : 'var(--text-primary)' }}>
                    {r.title}
                  </span>
                </div>
                <span style={{ fontSize: '0.74rem', color: 'var(--text-muted)' }}>{r.time}</span>
              </div>
            ))}
          </div>

          <div style={{ marginTop: '14px', textAlign: 'right' }}>
            <button onClick={() => navigate('/reminders')} className="btn btn-outline btn-sm">
              Manage All Tasks ({reminders.length}) →
            </button>
          </div>
        </div>

        {/* Cycle Length Variance Visualizer */}
        <div className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
            <h3 style={{ fontSize: '1.08rem', color: 'var(--text-primary)', margin: 0 }}>
              📈 Menstrual Interval History
            </h3>
            <span className="badge badge-warning">PCOS Variance</span>
          </div>
          <p style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginBottom: '14px' }}>
            Cycle intervals fluctuate naturally with PCOS. Typical regular range is 28-35 days:
          </p>

          <div style={{ display: 'flex', alignItems: 'flex-end', gap: '16px', height: '110px', paddingBottom: '8px', borderBottom: '1px solid var(--border-subtle)' }}>
            {cycleIntervalHistory.map((item, idx) => {
              const heightPct = Math.min(100, Math.max(30, (item.days / 50) * 100));
              const isOver = item.days > 35;
              return (
                <div key={idx} style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '4px' }}>
                  <span style={{ fontSize: '0.74rem', fontWeight: 700, color: isOver ? 'var(--coral-600)' : 'var(--primary-700)' }}>
                    {item.days}d
                  </span>
                  <div
                    style={{
                      width: '100%',
                      maxWidth: '38px',
                      height: `${heightPct}px`,
                      background: isOver
                        ? 'linear-gradient(180deg, var(--coral-500), var(--coral-600))'
                        : 'linear-gradient(180deg, var(--primary-500), var(--primary-700))',
                      borderRadius: '4px 4px 0 0',
                      transition: 'height 0.4s ease'
                    }}
                  />
                  <span style={{ fontSize: '0.68rem', color: 'var(--text-muted)', textAlign: 'center' }}>
                    {item.label.split(' ')[0]}
                  </span>
                </div>
              );
            })}
          </div>

          <div style={{ marginTop: '12px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span style={{ fontSize: '0.74rem', color: 'var(--text-muted)' }}>
              Target Window: 28–35 days
            </span>
            <button onClick={() => navigate('/cycle')} className="btn btn-outline btn-sm">
              View Calendar →
            </button>
          </div>
        </div>
      </div>

      {/* Quick Action Matrix */}
      <div style={{ marginBottom: '28px' }}>
        <h2 style={{ fontSize: '1.25rem', color: 'var(--text-primary)', marginBottom: '14px' }}>
          {isTelugu ? 'ముఖ్యమైన చర్యలు (Quick Actions)' : 'Quick Actions for Your Journey'}
        </h2>
        <div className="grid-3">
          <div
            className="card"
            onClick={() => navigate('/reports')}
            style={{ cursor: 'pointer', transition: 'all var(--transition-fast)' }}
          >
            <div style={{ fontSize: '2rem', marginBottom: '8px' }}>📄</div>
            <h4 style={{ fontSize: '1.02rem', color: 'var(--text-primary)', marginBottom: '4px' }}>
              Upload Medical Report
            </h4>
            <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>
              Scan blood tests or thyroid panels and translate medical terms into plain English.
            </p>
          </div>

          <div
            className="card"
            onClick={() => navigate('/food')}
            style={{ cursor: 'pointer', transition: 'all var(--transition-fast)' }}
          >
            <div style={{ fontSize: '2rem', marginBottom: '8px' }}>🍲</div>
            <h4 style={{ fontSize: '1.02rem', color: 'var(--text-primary)', marginBottom: '4px' }}>
              Explore Indian Meals
            </h4>
            <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>
              Find protein-balanced recipes like Pesarattu, Dal, and Korralu millets.
            </p>
          </div>

          <div
            className="card"
            onClick={() => navigate('/doctor-prep')}
            style={{ cursor: 'pointer', transition: 'all var(--transition-fast)' }}
          >
            <div style={{ fontSize: '2rem', marginBottom: '8px' }}>🩺</div>
            <h4 style={{ fontSize: '1.02rem', color: 'var(--text-primary)', marginBottom: '4px' }}>
              Doctor Visit Preparation
            </h4>
            <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>
              Synthesize symptoms and lab history into a 1-page printable consultation summary.
            </p>
          </div>
        </div>
      </div>

      {/* Today's Meal & Consultation Spotlight */}
      <div className="grid-2">
        {/* Today's Meal Plan Card */}
        <div className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '14px' }}>
            <h3 style={{ fontSize: '1.08rem', color: 'var(--text-primary)', margin: 0 }}>
              🍲 Today's Meal Plan Spotlight
            </h3>
            <span className="badge badge-primary">South Indian</span>
          </div>
          {dailyPlan.breakfast ? (
            <div style={{ background: 'var(--bg-subtle)', padding: '14px', borderRadius: 'var(--radius-md)' }}>
              <div style={{ fontWeight: 700, fontSize: '0.92rem', color: 'var(--text-primary)' }}>
                {dailyPlan.breakfast.image} {dailyPlan.breakfast.name}
              </div>
              <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: '4px' }}>
                {dailyPlan.breakfast.proteinSources} • {dailyPlan.breakfast.approxCalories}
              </div>
              <p style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', marginTop: '8px', lineHeight: 1.5 }}>
                {dailyPlan.breakfast.balancedExplanation}
              </p>
            </div>
          ) : (
            <div style={{ padding: '20px 0', textAlign: 'center', color: 'var(--text-muted)', fontSize: '0.86rem' }}>
              No breakfast chosen yet. Explore the Food Companion to add to your plan.
            </div>
          )}
          <div style={{ marginTop: '14px', textAlign: 'right' }}>
            <button onClick={() => navigate('/food')} className="btn btn-outline btn-sm">
              Manage Meals →
            </button>
          </div>
        </div>

        {/* Doctor Consultation Preparation Card */}
        <div className="card" style={{ background: 'var(--lavender-50)', border: '1px solid var(--lavender-200)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '14px' }}>
            <h3 style={{ fontSize: '1.08rem', color: 'var(--lavender-700)', margin: 0 }}>
              🩺 Clinical Visit Ready?
            </h3>
            <span className="badge badge-lavender">1-Page Sheet</span>
          </div>
          <p style={{ fontSize: '0.86rem', color: 'var(--text-secondary)', lineHeight: 1.6, marginBottom: '14px' }}>
            Your doctor appointment summary combines your recorded 38-day cycle interval, elevated TSH lab report, and key questions to ask regarding insulin resistance.
          </p>
          <div style={{ display: 'flex', gap: '10px' }}>
            <button onClick={() => navigate('/doctor-prep')} className="btn btn-secondary btn-sm" style={{ flex: 1 }}>
              Review Consultation Sheet
            </button>
            <button onClick={() => navigate('/assistant')} className="btn btn-outline btn-sm">
              Practice Questions
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
