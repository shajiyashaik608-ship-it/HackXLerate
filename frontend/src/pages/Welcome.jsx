import React from 'react';
import { useNavigate } from 'react-router-dom';

export default function Welcome({ language, onStartOnboarding, onOpenAuth }) {
  const navigate = useNavigate();
  const isTelugu = language === 'te';

  const features = [
    {
      icon: '🌸',
      title: isTelugu ? 'పీరియడ్ సైకిల్ ట్రాకింగ్' : 'Menstrual Cycle Intelligence',
      description: isTelugu
        ? 'PCOS సైకిల్స్ లోని సహజమైన హెచ్చుతగ్గులను అర్థం చేసుకునే పారదర్శక సైకిల్ విశ్లేషణ.'
        : 'Transparent cycle tracking that models natural PCOS variability (±4-6 days) rather than false exact dates.'
    },
    {
      icon: '🍲',
      title: isTelugu ? 'భారతీయ ఆహార సహచరుడు' : 'Indian PCOS Food Companion',
      description: isTelugu
        ? 'మన ఇళ్లలో చేసుకునే పెసరట్టు, కొర్రలు, పప్పు, రాగి వంటి పోషకాహార సూచనలు.'
        : 'Familiar, affordable Indian pantry staples (Pesarattu, Millets, Dal, Ragi) supporting healthy glucose stability.'
    },
    {
      icon: '🎙️',
      title: isTelugu ? 'తెలుగు & ఇంగ్లీష్ AI అసిస్టెంట్' : 'Bilingual AI Voice Saathi',
      description: isTelugu
        ? 'మీ సందేహాలను మీ సొంత భాషలో అడగండి, శ్రవణ సహాయంతో వివరాలు వినండి.'
        : 'Ask health-education questions in Telugu or English with browser voice speech-to-text and audio playback.'
    },
    {
      icon: '📄',
      title: isTelugu ? 'వైద్య రికార్డుల వివరణ' : 'Medical Record Intelligence',
      description: isTelugu
        ? 'రక్త పరీక్షలు, థైరాయిడ్, అల్ట్రాసౌండ్ రిపోర్టుల విలువలను సులభంగా అర్థం చేసుకోండి.'
        : 'Organize lab tests, benchmark reference ranges, and decode clinical terminology into plain language.'
    },
    {
      icon: '🩺',
      title: isTelugu ? 'డాక్టర్ విజిట్ ప్రిపరేషన్' : 'Doctor Consultation Prep',
      description: isTelugu
        ? 'మీ పీరియడ్స్, లక్షణాలు, రిపోర్టులతో 1-పేజీ సారాంశాన్ని ప్రింట్ చేసుకుని డాక్టర్‌కి చూపించండి.'
        : 'Synthesize symptoms, lab flags, and high-yield questions into an appointment-ready 1-page clinical brief.'
    },
    {
      icon: '💬',
      title: isTelugu ? 'రక్షిత కమ్యూనిటీ' : 'Safe PCOS Community',
      description: isTelugu
        ? 'అనామక పేరుతో సందేహాలు అడగండి, నిర్ధారిత వైద్య నిపుణుల సలహాలు చదవండి.'
        : 'An anonymous, moderated educational Q&A board free from unsafe cure claims or commercial marketing.'
    }
  ];

  return (
    <div style={{ maxWidth: '1120px', margin: '0 auto', padding: '40px 20px 80px 20px' }}>
      {/* Hero Container */}
      <div style={{
        background: 'linear-gradient(135deg, var(--primary-800) 0%, var(--primary-900) 100%)',
        borderRadius: 'var(--radius-xl)',
        padding: '50px 40px',
        color: '#ffffff',
        textAlign: 'center',
        boxShadow: '0 20px 40px -10px rgba(15, 118, 110, 0.3)',
        marginBottom: '48px',
        position: 'relative',
        overflow: 'hidden'
      }}>
        <div style={{
          display: 'inline-flex',
          alignItems: 'center',
          gap: '8px',
          background: 'rgba(255, 255, 255, 0.15)',
          padding: '6px 16px',
          borderRadius: 'var(--radius-full)',
          fontSize: '0.84rem',
          fontWeight: 600,
          marginBottom: '20px'
        }}>
          <span>🌿</span>
          <span>{isTelugu ? 'వ్యక్తిగత ఆరోగ్య సాథి' : 'AI-Powered Personal Health Copilot'}</span>
          <span style={{ opacity: 0.8 }}>• Hackathon Edition</span>
        </div>

        <h1 style={{ fontSize: '2.8rem', color: '#ffffff', marginBottom: '14px', lineHeight: 1.15 }}>
          PCOS Saathi
        </h1>
        <p style={{ fontSize: '1.2rem', color: 'var(--primary-100)', marginBottom: '10px', fontWeight: 500 }}>
          {isTelugu ? 'PCOS సంరక్షణలో మీ నమ్మకమైన నేస్తం' : 'Your Personal Companion for PCOS Care'}
        </p>
        <p style={{ maxWidth: '720px', margin: '0 auto 32px auto', fontSize: '0.98rem', color: '#e2e8f0', lineHeight: 1.6 }}>
          {isTelugu
            ? 'మీ ఆరోగ్య రికార్డులను ఒకే చోట నిర్వహించండి, సైకిల్స్ ట్రాక్ చేయండి, పోషకాహార సూచనలు పొందండి మరియు వైద్యుల సంప్రదింపులకు సులభంగా సిద్ధమవ్వండి.'
            : 'Consolidate medical documents, decode lab terminology, explore sustainable Indian meals, and prepare high-yield questions for your next clinical appointment.'}
        </p>

        <div style={{ display: 'flex', justifyContent: 'center', gap: '14px', flexWrap: 'wrap' }}>
          <button
            onClick={onStartOnboarding ? onStartOnboarding : () => navigate('/dashboard')}
            className="btn btn-coral btn-lg"
            style={{ borderRadius: 'var(--radius-full)', padding: '14px 32px' }}
          >
            {isTelugu ? 'ప్రారంభించండి (Get Started)' : 'Get Started & Setup Profile'}
          </button>
          <button
            onClick={() => navigate('/dashboard')}
            className="btn btn-outline btn-lg"
            style={{ borderRadius: 'var(--radius-full)', color: '#ffffff', borderColor: 'rgba(255,255,255,0.4)' }}
          >
            {isTelugu ? 'డెమో పరిశీలించండి' : 'Explore Interactive Demo'}
          </button>
          {onOpenAuth && (
            <button
              onClick={onOpenAuth}
              className="btn btn-ghost btn-lg"
              style={{ borderRadius: 'var(--radius-full)', color: 'var(--primary-200)', border: '1px dashed rgba(255,255,255,0.3)' }}
            >
              👤 Switch Demo Persona
            </button>
          )}
        </div>
      </div>

      {/* Feature Highlights Grid */}
      <div style={{ marginBottom: '48px' }}>
        <div style={{ textAlign: 'center', marginBottom: '32px' }}>
          <h2 style={{ fontSize: '1.8rem', color: 'var(--text-primary)', marginBottom: '8px' }}>
            {isTelugu ? 'సాథి ముఖ్య విశేషాలు' : 'Designed for Real-World Indian Healthcare'}
          </h2>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.95rem' }}>
            Empathetic, evidence-grounded tools built around the lived experience of managing PCOS.
          </p>
        </div>

        <div className="grid-3">
          {features.map((f, i) => (
            <div key={i} className="card" style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              <div style={{ fontSize: '2.2rem' }}>{f.icon}</div>
              <h3 style={{ fontSize: '1.12rem', color: 'var(--text-primary)' }}>{f.title}</h3>
              <p style={{ fontSize: '0.86rem', color: 'var(--text-secondary)', lineHeight: 1.6 }}>
                {f.description}
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* Privacy & Clinical Ethics Statement */}
      <div style={{
        background: 'var(--bg-card)',
        border: '1px solid var(--border-card)',
        borderRadius: 'var(--radius-lg)',
        padding: '28px 32px',
        display: 'flex',
        gap: '20px',
        alignItems: 'flex-start',
        boxShadow: 'var(--shadow-card)'
      }}>
        <div style={{ fontSize: '2rem' }}>🛡️</div>
        <div>
          <h3 style={{ fontSize: '1.1rem', color: 'var(--text-primary)', marginBottom: '6px' }}>
            Privacy First & Educational Notice
          </h3>
          <p style={{ fontSize: '0.86rem', color: 'var(--text-secondary)', lineHeight: 1.6, marginBottom: '8px' }}>
            PCOS Saathi operates strictly within your local browser for this demonstration. Your health data, cycle logs, and uploaded reports remain stored locally in your browser session.
          </p>
          <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)', fontStyle: 'italic' }}>
            <strong>Medical Disclaimer:</strong> This application provides health education and care organization assistance. It is NOT a medical diagnosis tool, does not claim to cure PCOS, and does not replace the judgment of certified healthcare practitioners.
          </p>
        </div>
      </div>
    </div>
  );
}
