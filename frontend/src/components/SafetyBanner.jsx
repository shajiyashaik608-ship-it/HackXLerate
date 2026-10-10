import React from 'react';

export default function SafetyBanner({ language = 'en' }) {
  const isTelugu = language === 'te';

  return (
    <div style={{
      background: '#fef3c7',
      borderBottom: '1px solid #fde68a',
      padding: '8px 20px',
      fontSize: '0.8rem',
      color: '#92400e',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      gap: '8px',
      textAlign: 'center'
    }}>
      <span style={{ fontSize: '1rem' }}>🛡️</span>
      <span>
        {isTelugu ? (
          <>
            <strong>వైద్య గమనిక:</strong> హెల్త్ సాథి సమాచారం కేవలం అవగాహన కొరకు మాత్రమే. ఇది వ్యాధి నిర్ధారణ (diagnosis) కాదు. చికిత్స కోసం మీ వైద్యుని సంప్రదించండి.
          </>
        ) : (
          <>
            <strong>Clinical Notice:</strong> Health Saathi is an educational health copilot. It does not diagnose or cure conditions. Always consult a certified healthcare practitioner.
          </>
        )}
      </span>
    </div>
  );
}
