import React from 'react';
import { SAMPLE_QUESTIONS } from '../../data/sampleQuestions';

export default function QuickQuestions({ language = 'en', onSelectQuestion }) {
  const questions = SAMPLE_QUESTIONS[language] || SAMPLE_QUESTIONS.en;

  return (
    <div style={{ marginBottom: '14px' }}>
      <div style={{ fontSize: '0.78rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: '8px' }}>
        {language === 'te' ? '💡 సూచించబడిన ప్రశ్నలు:' : '💡 Suggested health questions:'}
      </div>
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
        {questions.map((q) => (
          <button
            key={q.id}
            type="button"
            onClick={() => onSelectQuestion(q.text)}
            style={{
              background: 'var(--bg-card)',
              border: '1px solid var(--border-card)',
              padding: '6px 14px',
              borderRadius: 'var(--radius-full)',
              fontSize: '0.8rem',
              color: 'var(--text-secondary)',
              cursor: 'pointer',
              boxShadow: 'var(--shadow-sm)',
              transition: 'all var(--transition-fast)'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.borderColor = 'var(--primary-600)';
              e.currentTarget.style.color = 'var(--primary-700)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.borderColor = 'var(--border-card)';
              e.currentTarget.style.color = 'var(--text-secondary)';
            }}
          >
            💬 {q.text}
          </button>
        ))}
      </div>
    </div>
  );
}
