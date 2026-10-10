import React, { useState } from 'react';
import Modal from './Modal';
import FormField from './FormField';

export default function OnboardingModal({
  isOpen,
  onClose,
  language,
  setLanguage,
  profile,
  setProfile,
  onComplete
}) {
  const [step, setStep] = useState(1);
  const isTelugu = language === 'te';

  if (!isOpen) return null;

  const handleNext = () => {
    if (step < 3) {
      setStep(step + 1);
    } else {
      if (onComplete) onComplete();
      onClose();
    }
  };

  const handleSkip = () => {
    if (onComplete) onComplete();
    onClose();
  };

  return (
    <Modal
      isOpen={isOpen}
      onClose={handleSkip}
      title={
        step === 1 ? '🌿 Welcome to PCOS Saathi' :
        step === 2 ? '🛡️ Privacy, Consent & Educational Purpose' :
        '🌸 Personalize Your Health Baseline'
      }
      maxWidth="580px"
      footer={
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', width: '100%' }}>
          <button onClick={handleSkip} className="btn btn-ghost btn-sm" style={{ color: 'var(--text-muted)' }}>
            {isTelugu ? 'దాటవేయి (Skip Demo Setup)' : 'Skip Onboarding'}
          </button>
          <div style={{ display: 'flex', gap: '8px' }}>
            {step > 1 && (
              <button onClick={() => setStep(step - 1)} className="btn btn-outline btn-sm">
                Back
              </button>
            )}
            <button onClick={handleNext} className="btn btn-primary btn-sm">
              {step === 3 ? (isTelugu ? 'ప్రారంభించండి' : 'Finish & Open App') : (isTelugu ? 'తదుపరి' : 'Continue →')}
            </button>
          </div>
        </div>
      }
    >
      <div>
        {/* Step indicator */}
        <div style={{ display: 'flex', gap: '8px', marginBottom: '20px' }}>
          {[1, 2, 3].map((s) => (
            <div
              key={s}
              style={{
                flex: 1,
                height: '4px',
                borderRadius: '2px',
                backgroundColor: s <= step ? 'var(--primary-700)' : 'var(--border-subtle)',
                transition: 'all 0.3s ease'
              }}
            />
          ))}
        </div>

        {/* Step 1: Welcome & Language */}
        {step === 1 && (
          <div>
            <div style={{ textAlign: 'center', marginBottom: '20px' }}>
              <div style={{ fontSize: '2.5rem', marginBottom: '8px' }}>🌿</div>
              <h3 style={{ fontSize: '1.25rem', color: 'var(--text-primary)', marginBottom: '6px' }}>
                {isTelugu ? 'ఆరోగ్య సాథికి స్వాగతం' : 'Your Personal PCOS Health Copilot'}
              </h3>
              <p style={{ fontSize: '0.86rem', color: 'var(--text-secondary)', lineHeight: 1.5 }}>
                {isTelugu
                  ? 'వైద్య రిపోర్టులను అర్థం చేసుకోవడానికి, పీరియడ్ సైకిల్స్ మరియు భారతీయ ఆహార సమతుల్యతను పర్యవేక్షించడానికి మీ నేస్తం.'
                  : 'Empathetic, evidence-grounded health organization: understand medical reports, monitor cycles with natural variance, and plan familiar Indian meals.'}
              </p>
            </div>

            <div className="card" style={{ background: 'var(--bg-subtle)', padding: '16px', marginBottom: '16px' }}>
              <label style={{ display: 'block', fontSize: '0.84rem', fontWeight: 600, marginBottom: '10px' }}>
                Select Preferred Language / ప్రాధాన్యత భాష
              </label>
              <div style={{ display: 'flex', gap: '12px' }}>
                <button
                  type="button"
                  onClick={() => setLanguage('en')}
                  className={`btn ${language === 'en' ? 'btn-primary' : 'btn-outline'}`}
                  style={{ flex: 1 }}
                >
                  English (EN)
                </button>
                <button
                  type="button"
                  onClick={() => setLanguage('te')}
                  className={`btn ${language === 'te' ? 'btn-primary' : 'btn-outline'}`}
                  style={{ flex: 1 }}
                >
                  తెలుగు (Telugu - Voice Ready)
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Step 2: Consent & Safety */}
        {step === 2 && (
          <div>
            <div style={{
              background: 'var(--coral-50)',
              border: '1px solid var(--coral-500)',
              borderRadius: 'var(--radius-md)',
              padding: '16px',
              marginBottom: '16px',
              fontSize: '0.84rem',
              color: 'var(--coral-900)',
              lineHeight: 1.6
            }}>
              <strong>⚠️ Educational & Demonstration Guardrail:</strong>
              <ul style={{ paddingLeft: '20px', marginTop: '6px' }}>
                <li>This application is strictly for health education and clinical visit preparation.</li>
                <li>It does NOT issue medical diagnoses or alter medication dosages.</li>
                <li>Menstrual predictions model natural variance (±4-6 days) and are not guaranteed arrival dates.</li>
                <li>Severe pain or heavy bleeding requires immediate emergency hospital care.</li>
              </ul>
            </div>

            <div style={{
              background: 'var(--bg-subtle)',
              padding: '14px',
              borderRadius: 'var(--radius-md)',
              fontSize: '0.82rem',
              color: 'var(--text-secondary)',
              lineHeight: 1.5
            }}>
              🔒 <strong>Browser-Only Privacy:</strong> All entered health profiles, reminder schedules, and uploaded files are stored locally in your browser's <code>localStorage</code> sandbox for this hackathon evaluation. No medical data is transmitted to external servers.
            </div>
          </div>
        )}

        {/* Step 3: Basic Profile */}
        {step === 3 && (
          <div>
            <p style={{ fontSize: '0.84rem', color: 'var(--text-muted)', marginBottom: '16px' }}>
              Optionally configure your initial baseline (you can change this at any time in Profile settings):
            </p>

            <FormField
              label="Your Preferred Name"
              id="onboard-name"
              value={profile.name}
              onChange={(e) => setProfile({ ...profile, name: e.target.value })}
              placeholder="e.g. Priya"
            />

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '14px' }}>
              <FormField
                label="Age"
                id="onboard-age"
                type="number"
                value={profile.age}
                onChange={(e) => setProfile({ ...profile, age: Number(e.target.value) })}
              />
              <FormField
                label="Average Cycle (Days)"
                id="onboard-cycle"
                type="number"
                value={profile.cycleLength}
                onChange={(e) => setProfile({ ...profile, cycleLength: Number(e.target.value) })}
                hint="Typical PCOS range: 30-45 days"
              />
            </div>

            <div className="form-group" style={{ marginBottom: '16px' }}>
              <label className="form-label" style={{ display: 'block', fontSize: '0.84rem', fontWeight: 600, marginBottom: '6px' }}>
                Dietary Preference (For Indian Food Companion)
              </label>
              <select
                value={profile.dietType}
                onChange={(e) => setProfile({ ...profile, dietType: e.target.value })}
                style={{ width: '100%' }}
              >
                <option value="vegetarian">Vegetarian (Lacto-veg)</option>
                <option value="egg">Eggetarian</option>
                <option value="all">Non-Vegetarian (Include fish/chicken)</option>
              </select>
            </div>
          </div>
        )}
      </div>
    </Modal>
  );
}
