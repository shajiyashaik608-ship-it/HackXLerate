import React, { useState } from 'react';
import Modal from './Modal';
import FormField from './FormField';

export const DEMO_PERSONAS = [
  {
    id: 'priya',
    name: 'Priya Sharma',
    age: 24,
    dietType: 'vegetarian',
    cycleLength: 33,
    periodDuration: 4,
    wellnessGoals: 'Manage insulin resistance and establish predictable menstrual cycles.'
  },
  {
    id: 'ananya',
    name: 'Ananya Rao',
    age: 29,
    dietType: 'egg',
    cycleLength: 42,
    periodDuration: 5,
    wellnessGoals: 'Improve energy levels, reduce luteal fatigue, and prepare for endocrinologist consultation.'
  },
  {
    id: 'guest',
    name: 'Guest Explorer',
    age: 26,
    dietType: 'all',
    cycleLength: 30,
    periodDuration: 4,
    wellnessGoals: 'Evaluating Health Saathi PCOS educational copilot.'
  }
];

export default function AuthModal({
  isOpen,
  onClose,
  currentUser,
  onSelectPersona,
  onLogout
}) {
  const [tab, setTab] = useState('demo'); // 'demo', 'signin', 'signup'
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');

  if (!isOpen) return null;

  const handleCustomAuth = (e) => {
    e.preventDefault();
    onSelectPersona({
      name: name.trim() || email.split('@')[0] || 'Demo User',
      age: 25,
      dietType: 'vegetarian',
      cycleLength: 32,
      periodDuration: 4,
      wellnessGoals: 'Active user session'
    });
    onClose();
  };

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title="🔐 Demo Access & Persona Switcher"
      maxWidth="500px"
    >
      <div>
        {/* Notice */}
        <div style={{
          background: 'var(--primary-50)',
          border: '1px solid var(--primary-200)',
          borderRadius: 'var(--radius-md)',
          padding: '12px 14px',
          fontSize: '0.8rem',
          color: 'var(--primary-900)',
          marginBottom: '16px',
          lineHeight: 1.5
        }}>
          💡 <strong>Simulated Authentication Notice:</strong> This prototype runs client-side for hackathon evaluation without storing plaintext credentials or connecting to real identity providers. Backend FastAPI endpoints (`/api/v1/auth/login`) are architected for production.
        </div>

        {/* Tab Switcher */}
        <div style={{ display: 'flex', gap: '8px', borderBottom: '1px solid var(--border-subtle)', paddingBottom: '12px', marginBottom: '16px' }}>
          <button
            onClick={() => setTab('demo')}
            className={`btn btn-sm ${tab === 'demo' ? 'btn-primary' : 'btn-outline'}`}
          >
            Switch Demo Persona
          </button>
          <button
            onClick={() => setTab('signin')}
            className={`btn btn-sm ${tab === 'signin' ? 'btn-primary' : 'btn-outline'}`}
          >
            Custom Sign In
          </button>
          <button
            onClick={() => setTab('signup')}
            className={`btn btn-sm ${tab === 'signup' ? 'btn-primary' : 'btn-outline'}`}
          >
            Sign Up
          </button>
        </div>

        {tab === 'demo' ? (
          <div>
            <p style={{ fontSize: '0.84rem', color: 'var(--text-muted)', marginBottom: '14px' }}>
              Choose a simulated patient profile to evaluate personalized cycle states, meal plans, and consultation briefs:
            </p>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
              {DEMO_PERSONAS.map((p) => {
                const isCurrent = currentUser?.name === p.name;
                return (
                  <div
                    key={p.id}
                    onClick={() => {
                      onSelectPersona(p);
                      onClose();
                    }}
                    style={{
                      border: `1px solid ${isCurrent ? 'var(--primary-600)' : 'var(--border-subtle)'}`,
                      background: isCurrent ? 'var(--primary-50)' : 'var(--bg-subtle)',
                      borderRadius: 'var(--radius-md)',
                      padding: '12px 16px',
                      cursor: 'pointer',
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center',
                      transition: 'all 0.15s ease'
                    }}
                  >
                    <div>
                      <div style={{ fontWeight: 700, fontSize: '0.92rem', color: 'var(--text-primary)' }}>
                        {p.name} (Age {p.age})
                      </div>
                      <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginTop: '2px' }}>
                        Cycle: {p.cycleLength}d • Diet: {p.dietType}
                      </div>
                      <div style={{ fontSize: '0.74rem', color: 'var(--text-secondary)', marginTop: '4px' }}>
                        🎯 {p.wellnessGoals}
                      </div>
                    </div>
                    {isCurrent ? (
                      <span className="badge badge-success" style={{ fontSize: '0.7rem' }}>Active</span>
                    ) : (
                      <span className="btn btn-outline btn-sm" style={{ fontSize: '0.75rem', padding: '4px 8px' }}>Select</span>
                    )}
                  </div>
                );
              })}
            </div>

            {currentUser && (
              <div style={{ marginTop: '18px', textAlign: 'center', borderTop: '1px solid var(--border-subtle)', paddingTop: '14px' }}>
                <button onClick={onLogout} className="btn btn-ghost btn-sm" style={{ color: 'var(--coral-600)' }}>
                  🚪 Sign Out of Demo Session
                </button>
              </div>
            )}
          </div>
        ) : (
          <form onSubmit={handleCustomAuth}>
            {tab === 'signup' && (
              <FormField
                label="Full Name"
                id="auth-name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="e.g. Radhika Sen"
                required
              />
            )}
            <FormField
              label="Email Address"
              id="auth-email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="demo@healthsaathi.in"
              required
            />
            <FormField
              label="Password (Simulated)"
              id="auth-password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              hint="Any test password accepted in frontend demo mode."
              required
            />
            <div style={{ marginTop: '18px', display: 'flex', gap: '10px', justifyContent: 'flex-end' }}>
              <button type="button" onClick={onClose} className="btn btn-outline btn-sm">
                Cancel
              </button>
              <button type="submit" className="btn btn-primary btn-sm">
                {tab === 'signin' ? 'Sign In (Demo)' : 'Create Demo Account'}
              </button>
            </div>
          </form>
        )}
      </div>
    </Modal>
  );
}
