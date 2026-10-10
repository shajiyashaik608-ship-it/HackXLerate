import React from 'react';
import PageHeader from '../components/PageHeader';
import ChatWindow from '../features/assistant/ChatWindow';

export default function HealthAssistant({
  language,
  setLanguage,
  chatHistory,
  setChatHistory
}) {
  const isTelugu = language === 'te';

  return (
    <div style={{ maxWidth: '980px', margin: '0 auto' }}>
      <PageHeader
        title={isTelugu ? 'AI హెల్త్ అసిస్టెంట్ (PCOS సాథి)' : 'AI Health Assistant — PCOS Saathi'}
        subtitle={isTelugu
          ? 'మీ ఆరోగ్య సందేహాలను తెలుగు లేదా ఇంగ్లీష్ లో అడగండి. నిపుణుల మార్గదర్శకాల ఆధారంగా రూపొందించబడింది.'
          : 'Ask health-education questions in Telugu or English with browser voice recognition and spoken audio explanations.'}
        badge="Bilingual Voice Ready"
      />

      {/* Safety Notice */}
      <div style={{
        background: 'var(--accent-yellow-light)',
        border: '1px solid var(--accent-yellow)',
        borderRadius: 'var(--radius-md)',
        padding: '12px 18px',
        marginBottom: '20px',
        fontSize: '0.82rem',
        color: '#854d0e',
        display: 'flex',
        alignItems: 'center',
        gap: '10px'
      }}>
        <span style={{ fontSize: '1.2rem' }}>🛡️</span>
        <span>
          <strong>Clinical Education Notice:</strong> PCOS Saathi explains terms and provides general health awareness. It does not replace the professional advice of a certified physician and does not provide formal diagnosis or prescription modifications.
        </span>
      </div>

      <ChatWindow
        language={language}
        setLanguage={setLanguage}
        chatHistory={chatHistory}
        setChatHistory={setChatHistory}
      />
    </div>
  );
}
