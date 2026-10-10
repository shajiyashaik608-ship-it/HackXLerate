import React from 'react';
import { NavLink, Link } from 'react-router-dom';

export default function Sidebar({ language = 'en', profile, onOpenAuth }) {
  const isTelugu = language === 'te';

  const navLinks = [
    { to: '/dashboard', label: isTelugu ? 'డాష్‌బోర్డ్' : 'Dashboard', icon: '📊' },
    { to: '/reports', label: isTelugu ? 'మెడికల్ రిపోర్ట్స్' : 'Medical Reports', icon: '📄' },
    { to: '/food', label: isTelugu ? 'ఇండియన్ ఫుడ్' : 'Food Companion', icon: '🍲' },
    { to: '/assistant', label: isTelugu ? 'AI సాథి అసిస్టెంట్' : 'AI Health Assistant', icon: '🎙️' },
    { to: '/cycle', label: isTelugu ? 'పీరియడ్ ట్రాకర్' : 'Cycle Tracker', icon: '🌸' },
    { to: '/doctor-prep', label: isTelugu ? 'డాక్టర్ ప్రిపరేషన్' : 'Doctor Visit Prep', icon: '🩺' },
    { to: '/reminders', label: isTelugu ? 'కేర్ రిమైండర్లు' : 'Smart Reminders', icon: '⏰' },
    { to: '/community', label: isTelugu ? 'కమ్యూనిటీ' : 'PCOS Community', icon: '💬' },
    { to: '/profile', label: isTelugu ? 'హెల్త్ ప్రొఫైల్' : 'Health Profile', icon: '👤' },
    { to: '/settings', label: isTelugu ? 'సెట్టింగ్స్' : 'Settings', icon: '⚙️' }
  ];

  return (
    <aside className="app-sidebar" style={{
      width: 'var(--sidebar-width)',
      backgroundColor: 'var(--bg-card)',
      borderRight: '1px solid var(--border-subtle)',
      display: 'flex',
      flexDirection: 'column',
      height: '100vh',
      position: 'sticky',
      top: 0,
      zIndex: 40,
      flexShrink: 0
    }}>
      {/* Brand Header */}
      <div style={{
        padding: '22px 20px',
        borderBottom: '1px solid var(--border-subtle)',
        display: 'flex',
        alignItems: 'center',
        gap: '12px'
      }}>
        <Link to="/dashboard" style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <div style={{
            width: '42px',
            height: '42px',
            borderRadius: '12px',
            background: 'linear-gradient(135deg, var(--primary-700), var(--primary-900))',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: '1.3rem',
            color: '#ffffff',
            boxShadow: '0 4px 12px rgba(15, 118, 110, 0.25)'
          }}>
            🌿
          </div>
          <div>
            <div style={{ fontSize: '1.2rem', fontWeight: 800, color: 'var(--text-primary)', letterSpacing: '-0.02em', lineHeight: 1.1 }}>
              PCOS Saathi
            </div>
            <div style={{ fontSize: '0.72rem', color: 'var(--primary-700)', fontWeight: 600 }}>
              PERSONAL HEALTH COPILOT
            </div>
          </div>
        </Link>
      </div>

      {/* Nav Menu */}
      <nav style={{ flex: 1, padding: '16px 12px', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '4px' }}>
        {navLinks.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            className={({ isActive }) => `sidebar-link ${isActive ? 'active' : ''}`}
            style={({ isActive }) => ({
              display: 'flex',
              alignItems: 'center',
              gap: '12px',
              padding: '10px 14px',
              borderRadius: 'var(--radius-md)',
              fontSize: '0.88rem',
              fontWeight: isActive ? 700 : 500,
              color: isActive ? 'var(--primary-800)' : 'var(--text-secondary)',
              backgroundColor: isActive ? 'var(--primary-100)' : 'transparent',
              transition: 'all var(--transition-fast)'
            })}
          >
            <span style={{ fontSize: '1.15rem' }}>{item.icon}</span>
            <span>{item.label}</span>
          </NavLink>
        ))}
      </nav>

      {/* Footer Demo Persona & Ethics */}
      <div style={{
        padding: '14px 16px',
        borderTop: '1px solid var(--border-subtle)',
        backgroundColor: 'var(--bg-subtle)',
        fontSize: '0.75rem'
      }}>
        {profile && onOpenAuth && (
          <div
            onClick={onOpenAuth}
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              marginBottom: '10px',
              padding: '6px 8px',
              borderRadius: '6px',
              background: '#ffffff',
              border: '1px solid var(--border-subtle)',
              cursor: 'pointer'
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
              <span>👤</span>
              <span style={{ fontWeight: 600, color: 'var(--text-primary)' }}>{profile.name}</span>
            </div>
            <span style={{ color: 'var(--primary-700)', fontWeight: 600, fontSize: '0.7rem' }}>Switch</span>
          </div>
        )}
        <div style={{ color: 'var(--text-muted)', lineHeight: 1.35 }}>
          🛡️ <strong>Educational only:</strong> No diagnostic claims. Consult a certified doctor.
        </div>
      </div>
    </aside>
  );
}
