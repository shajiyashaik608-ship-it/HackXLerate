import React from 'react';
import { NavLink } from 'react-router-dom';

export default function MobileNavigation({ language }) {
  const isTelugu = language === 'te';

  const items = [
    { to: '/dashboard', label: isTelugu ? 'హోమ్' : 'Home', icon: '📊' },
    { to: '/cycle', label: isTelugu ? 'సైకిల్' : 'Cycle', icon: '🌸' },
    { to: '/assistant', label: isTelugu ? 'సాథి' : 'Saathi', icon: '🎙️' },
    { to: '/food', label: isTelugu ? 'ఆహారం' : 'Food', icon: '🍲' },
    { to: '/profile', label: isTelugu ? 'ప్రొఫైల్' : 'Profile', icon: '👤' }
  ];

  return (
    <nav className="mobile-bottom-nav" style={{
      position: 'fixed',
      bottom: 0,
      left: 0,
      right: 0,
      height: '64px',
      backgroundColor: 'var(--bg-card)',
      borderTop: '1px solid var(--border-subtle)',
      display: 'none', // Handled via responsive.css for screens <= 768px
      justifyContent: 'space-around',
      alignItems: 'center',
      zIndex: 50,
      boxShadow: '0 -4px 12px rgba(0, 0, 0, 0.05)'
    }}>
      {items.map((item) => (
        <NavLink
          key={item.to}
          to={item.to}
          style={({ isActive }) => ({
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: '0.72rem',
            fontWeight: isActive ? 700 : 500,
            color: isActive ? 'var(--primary-700)' : 'var(--text-muted)',
            textDecoration: 'none',
            flex: 1,
            padding: '4px 0'
          })}
        >
          <span style={{ fontSize: '1.25rem', marginBottom: '2px' }}>{item.icon}</span>
          <span>{item.label}</span>
        </NavLink>
      ))}
    </nav>
  );
}
