import React from 'react';

export default function Dashboard({ setActiveTab, language }) {
  const isTelugu = language === 'te';

  return (
    <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '24px 20px' }}>
      {/* Welcome Hero */}
      <div style={{
        background: 'linear-gradient(135deg, #0f766e 0%, #134e4a 100%)',
        borderRadius: '18px',
        padding: '30px',
        color: 'white',
        marginBottom: '28px',
        boxShadow: '0 10px 25px -5px rgba(15, 118, 110, 0.25)',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        flexWrap: 'wrap',
        gap: '20px'
      }}>
        <div style={{ maxWidth: '650px' }}>
          <div style={{
            display: 'inline-block',
            background: 'rgba(255, 255, 255, 0.2)',
            padding: '4px 12px',
            borderRadius: '999px',
            fontSize: '0.78rem',
            fontWeight: 600,
            marginBottom: '12px'
          }}>
            {isTelugu ? '🌿 మీ వ్యక్తిగత ఆరోగ్య సాథి' : '🌿 Personal Health Copilot & PCOS Companion'}
          </div>
          <h1 style={{ fontSize: '1.9rem', marginBottom: '8px', fontWeight: 700 }}>
            {isTelugu ? 'నమస్తే ప్రియ, మీ ఆరోగ్యం ఎలా ఉంది?' : 'Hello Priya, Welcome to Health Saathi'}
          </h1>
          <p style={{ opacity: 0.9, fontSize: '0.95rem', lineHeight: '1.6' }}>
            {isTelugu
              ? 'మీ రక్త పరీక్షల రిపోర్టులను అర్థం చేసుకోండి, స్థానిక ఆహార మార్గదర్శకాలను పొందండి మరియు తెలుగులో మీ సందేహాలు నివృత్తి చేసుకోండి.'
              : 'Empowering your care journey with medical report intelligence, authentic Indian nutrition, cautious cycle estimates, and Telugu voice assistance.'}
          </p>
        </div>

        <div style={{ display: 'flex', gap: '10px' }}>
          <button 
            onClick={() => setActiveTab('assistant')}
            className="btn-rose"
            style={{ borderRadius: '12px', padding: '12px 20px' }}
          >
            <span>🎙️</span>
            <span>{isTelugu ? 'తెలుగు అసిస్టెంట్' : 'PCOS Voice Saathi'}</span>
          </button>
        </div>
      </div>

      {/* Snapshot Cards */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
        gap: '20px',
        marginBottom: '28px'
      }}>
        {/* Cycle Snapshot */}
        <div className="glass-panel" style={{ padding: '22px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '14px' }}>
            <span style={{ fontSize: '1.5rem' }}>🌸</span>
            <span className="badge badge-normal">Day 14 (Follicular)</span>
          </div>
          <h3 style={{ fontSize: '1.05rem', color: '#0f172a', marginBottom: '6px' }}>Menstrual Cycle Status</h3>
          <p style={{ fontSize: '0.86rem', color: '#64748b', marginBottom: '12px' }}>
            Last cycle started on <strong>Sep 25</strong> (38-day gap).
          </p>
          <div style={{
            background: '#f8fafc',
            border: '1px dashed #cbd5e1',
            borderRadius: '10px',
            padding: '10px 12px',
            fontSize: '0.8rem',
            color: '#475569'
          }}>
            ⏱️ <strong>Estimated Next Window:</strong> Oct 28 - Nov 03 (±6 days variance).
          </div>
        </div>

        {/* Lab Intelligence Snapshot */}
        <div className="glass-panel" style={{ padding: '22px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '14px' }}>
            <span style={{ fontSize: '1.5rem' }}>📄</span>
            <span className="badge badge-elevated">Review Needed</span>
          </div>
          <h3 style={{ fontSize: '1.05rem', color: '#0f172a', marginBottom: '6px' }}>Latest Report Finding</h3>
          <p style={{ fontSize: '0.86rem', color: '#64748b', marginBottom: '12px' }}>
            TSH (Thyroid): <strong>4.8 mIU/L</strong> (Ref: 0.4 - 4.5).
          </p>
          <div style={{
            background: '#fef3c7',
            borderRadius: '10px',
            padding: '10px 12px',
            fontSize: '0.8rem',
            color: '#92400e'
          }}>
            💡 Slightly above standard range. Added to your Doctor Consultation Brief.
          </div>
        </div>

        {/* Care Reminder */}
        <div className="glass-panel" style={{ padding: '22px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '14px' }}>
            <span style={{ fontSize: '1.5rem' }}>⏰</span>
            <span className="badge badge-normal">Active Today</span>
          </div>
          <h3 style={{ fontSize: '1.05rem', color: '#0f172a', marginBottom: '6px' }}>Next Care Routine</h3>
          <p style={{ fontSize: '0.86rem', color: '#64748b', marginBottom: '12px' }}>
            <strong>Myo-Inositol sachet</strong> with lukewarm water at 8:30 PM.
          </p>
          <div style={{
            background: '#f0fdfa',
            borderRadius: '10px',
            padding: '10px 12px',
            fontSize: '0.8rem',
            color: '#0f766e'
          }}>
            👟 30-min evening brisk walk logged yesterday!
          </div>
        </div>
      </div>

      {/* Quick Action Matrix */}
      <h2 style={{ fontSize: '1.3rem', marginBottom: '16px', color: '#0f172a' }}>
        {isTelugu ? 'ముఖ్యమైన చర్యలు (Quick Actions)' : 'Key Actions for Your Care'}
      </h2>
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))',
        gap: '16px'
      }}>
        <div 
          onClick={() => setActiveTab('reports')}
          className="glass-panel" 
          style={{ padding: '20px', cursor: 'pointer', transition: 'all 0.2s' }}
        >
          <div style={{ fontSize: '2rem', marginBottom: '10px' }}>📄</div>
          <h4 style={{ fontSize: '1rem', marginBottom: '4px' }}>Upload Medical Report</h4>
          <p style={{ fontSize: '0.82rem', color: '#64748b' }}>Extract biomarkers and get plain-language explanations.</p>
        </div>

        <div 
          onClick={() => setActiveTab('food')}
          className="glass-panel" 
          style={{ padding: '20px', cursor: 'pointer', transition: 'all 0.2s' }}
        >
          <div style={{ fontSize: '2rem', marginBottom: '10px' }}>🍲</div>
          <h4 style={{ fontSize: '1rem', marginBottom: '4px' }}>Indian PCOS Food Companion</h4>
          <p style={{ fontSize: '0.82rem', color: '#64748b' }}>Familiar dishes (Pesarattu, Roti, Dal) with protein balance.</p>
        </div>

        <div 
          onClick={() => setActiveTab('doctor-prep')}
          className="glass-panel" 
          style={{ padding: '20px', cursor: 'pointer', transition: 'all 0.2s' }}
        >
          <div style={{ fontSize: '2rem', marginBottom: '10px' }}>🩺</div>
          <h4 style={{ fontSize: '1rem', marginBottom: '4px' }}>Doctor Visit Preparation</h4>
          <p style={{ fontSize: '0.82rem', color: '#64748b' }}>Generate a 1-page summary with symptoms & lab history.</p>
        </div>

        <div 
          onClick={() => setActiveTab('assistant')}
          className="glass-panel" 
          style={{ padding: '20px', cursor: 'pointer', transition: 'all 0.2s' }}
        >
          <div style={{ fontSize: '2rem', marginBottom: '10px' }}>🎙️</div>
          <h4 style={{ fontSize: '1rem', marginBottom: '4px' }}>PCOS Saathi (Telugu Voice)</h4>
          <p style={{ fontSize: '0.82rem', color: '#64748b' }}>Ask health questions in Telugu or English with audio playback.</p>
        </div>
      </div>
    </div>
  );
}
