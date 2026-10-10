import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import NotificationPanel from './NotificationPanel';

export default function Navbar({
  language,
  setLanguage,
  profile,
  notifications,
  onMarkNotificationAsRead,
  onClearNotifications,
  onToggleMobileNav,
  onOpenAuth
}) {
  const [showNotifPanel, setShowNotifPanel] = useState(false);
  const location = useLocation();

  const getPageTitle = (path) => {
    switch (path) {
      case '/dashboard': return language === 'te' ? 'డాష్‌బోర్డ్' : 'Dashboard Overview';
      case '/profile': return language === 'te' ? 'ఆరోగ్య ప్రొఫైల్' : 'My Health Profile';
      case '/assistant': return language === 'te' ? 'AI సాథి అసిస్టెంట్' : 'AI Health Assistant';
      case '/cycle': return language === 'te' ? 'సైకిల్ ట్రాకర్' : 'Menstrual Cycle Tracker';
      case '/food': return language === 'te' ? 'ఆహార సహచరుడు' : 'Indian Food PCOS Companion';
      case '/reports': return language === 'te' ? 'వైద్య రికార్డులు' : 'Medical Reports & Records';
      case '/doctor-prep': return language === 'te' ? 'డాక్టర్ సంప్రదింపు సారాంశం' : 'Doctor Visit Preparation';
      case '/reminders': return language === 'te' ? 'కేర్ రిమైండర్లు' : 'Smart Care Reminders';
      case '/community': return language === 'te' ? 'PCOS కమ్యూనిటీ' : 'Safe PCOS Community';
      case '/settings': return language === 'te' ? 'సెట్టింగ్స్' : 'Application Settings';
      case '/welcome': return language === 'te' ? 'స్వాగతం' : 'Welcome & Overview';
      default: return 'PCOS Saathi';
    }
  };

  const unreadCount = notifications.filter((n) => !n.read).length;

  return (
    <header style={{
      height: 'var(--navbar-height)',
      backgroundColor: 'var(--bg-card)',
      borderBottom: '1px solid var(--border-subtle)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      padding: '0 24px',
      position: 'sticky',
      top: 0,
      zIndex: 30
    }}>
      {/* Left: Mobile hamburger & Breadcrumb / Page Title */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
        <button
          onClick={onToggleMobileNav}
          className="btn btn-ghost btn-sm mobile-nav-toggle"
          style={{ fontSize: '1.25rem', padding: '6px' }}
          aria-label="Toggle navigation drawer"
        >
          ☰
        </button>

        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.72rem', color: 'var(--text-muted)' }}>
            <Link to="/dashboard" style={{ color: 'var(--primary-700)', fontWeight: 600 }}>Home</Link>
            <span>/</span>
            <span>{getPageTitle(location.pathname)}</span>
          </div>
          <h2 style={{ fontSize: '1.2rem', color: 'var(--text-primary)', fontWeight: 700, margin: 0, lineHeight: 1.2 }}>
            {getPageTitle(location.pathname)}
          </h2>
        </div>
      </div>

      {/* Right Controls */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
        {/* Language Switcher */}
        <div style={{
          display: 'flex',
          background: 'var(--bg-subtle)',
          borderRadius: 'var(--radius-sm)',
          padding: '2px',
          border: '1px solid var(--border-subtle)'
        }}>
          <button
            onClick={() => setLanguage('en')}
            style={{
              padding: '4px 10px',
              borderRadius: '6px',
              fontSize: '0.78rem',
              fontWeight: 600,
              background: language === 'en' ? '#ffffff' : 'transparent',
              color: language === 'en' ? 'var(--primary-700)' : 'var(--text-muted)',
              boxShadow: language === 'en' ? 'var(--shadow-sm)' : 'none'
            }}
          >
            EN
          </button>
          <button
            onClick={() => setLanguage('te')}
            style={{
              padding: '4px 10px',
              borderRadius: '6px',
              fontSize: '0.78rem',
              fontWeight: 600,
              background: language === 'te' ? '#ffffff' : 'transparent',
              color: language === 'te' ? 'var(--primary-700)' : 'var(--text-muted)',
              boxShadow: language === 'te' ? 'var(--shadow-sm)' : 'none'
            }}
          >
            తెలుగు
          </button>
        </div>

        {/* Notifications Icon Button */}
        <div style={{ position: 'relative' }}>
          <button
            onClick={() => setShowNotifPanel(!showNotifPanel)}
            className="btn btn-ghost"
            style={{
              position: 'relative',
              width: '38px',
              height: '38px',
              borderRadius: '50%',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '1.15rem',
              background: 'var(--bg-subtle)'
            }}
            title="Notifications"
          >
            🔔
            {unreadCount > 0 && (
              <span style={{
                position: 'absolute',
                top: '2px',
                right: '2px',
                width: '18px',
                height: '18px',
                borderRadius: '50%',
                background: 'var(--coral-600)',
                color: '#ffffff',
                fontSize: '0.65rem',
                fontWeight: 700,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
              }}>
                {unreadCount}
              </span>
            )}
          </button>

          {showNotifPanel && (
            <NotificationPanel
              notifications={notifications}
              onMarkAsRead={onMarkNotificationAsRead}
              onClearAll={onClearNotifications}
              onClose={() => setShowNotifPanel(false)}
            />
          )}
        </div>

        {/* Demo Persona Switcher Trigger */}
        <div
          onClick={onOpenAuth}
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            padding: '4px 10px 4px 6px',
            borderRadius: 'var(--radius-full)',
            background: 'var(--bg-subtle)',
            border: '1px solid var(--border-subtle)',
            cursor: 'pointer',
            transition: 'all 0.15s ease'
          }}
          title="Switch Demo Persona or Sign In"
        >
          <div style={{
            width: '28px',
            height: '28px',
            borderRadius: '50%',
            background: 'linear-gradient(135deg, var(--primary-700), var(--coral-500))',
            color: '#ffffff',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontWeight: 700,
            fontSize: '0.78rem'
          }}>
            {profile.name ? profile.name.charAt(0).toUpperCase() : 'P'}
          </div>
          <span style={{ fontSize: '0.82rem', fontWeight: 600, color: 'var(--text-primary)' }}>
            {profile.name || 'Priya'}
          </span>
          <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>▼</span>
        </div>
      </div>
    </header>
  );
}
