import React from 'react';
import { Link } from 'react-router-dom';

export default function NotFound() {
  return (
    <div style={{
      textAlign: 'center',
      padding: '80px 20px',
      maxWidth: '480px',
      margin: '0 auto'
    }}>
      <div style={{ fontSize: '3rem', marginBottom: '14px' }}>🌿</div>
      <h1 style={{ fontSize: '2rem', color: 'var(--text-primary)', marginBottom: '10px' }}>
        404 — Page Not Found
      </h1>
      <p style={{ fontSize: '0.92rem', color: 'var(--text-secondary)', marginBottom: '24px' }}>
        The health companion screen you are looking for does not exist or has been moved.
      </p>
      <Link to="/dashboard" className="btn btn-primary">
        Return to Dashboard Overview
      </Link>
    </div>
  );
}
