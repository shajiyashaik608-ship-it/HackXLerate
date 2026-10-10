import React, { useState } from 'react';
import { formatDisplayDate } from '../utils/dateUtils';

export default function CommunityPost({
  post,
  onVoteHelpful,
  onAddReply,
  onReport
}) {
  const [showReplies, setShowReplies] = useState(true);
  const [replyText, setReplyText] = useState('');

  const handleReplySubmit = (e) => {
    e.preventDefault();
    if (!replyText.trim()) return;
    onAddReply(post.id, replyText);
    setReplyText('');
  };

  return (
    <div className="card" style={{ marginBottom: '18px' }}>
      {/* Post Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <div style={{ width: '28px', height: '28px', borderRadius: '50%', background: 'var(--lavender-100)', color: 'var(--lavender-700)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '0.75rem', fontWeight: 700 }}>
            👤
          </div>
          <span style={{ fontSize: '0.82rem', fontWeight: 600, color: 'var(--text-secondary)' }}>
            {post.author}
          </span>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-light)' }}>
            • {formatDisplayDate(post.date)}
          </span>
        </div>
        <span className="badge badge-primary">{post.category}</span>
      </div>

      {/* Post Content */}
      <h3 style={{ fontSize: '1.15rem', color: 'var(--text-primary)', marginBottom: '8px', lineHeight: 1.4 }}>
        {post.title}
      </h3>
      <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', lineHeight: 1.6, marginBottom: '16px' }}>
        {post.content}
      </p>

      {/* Post Actions Bar */}
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        paddingTop: '12px',
        borderTop: '1px solid var(--border-subtle)',
        fontSize: '0.82rem',
        color: 'var(--text-muted)'
      }}>
        <div style={{ display: 'flex', gap: '12px' }}>
          <button
            onClick={() => onVoteHelpful(post.id)}
            className={`btn btn-sm ${post.userVoted ? 'btn-secondary' : 'btn-outline'}`}
            style={{ borderRadius: 'var(--radius-full)' }}
          >
            👍 Helpful ({post.helpfulCount})
          </button>
          <button
            onClick={() => setShowReplies(!showReplies)}
            className="btn btn-ghost btn-sm"
          >
            💬 Replies ({post.replies?.length || 0})
          </button>
        </div>

        <button
          onClick={() => onReport(post)}
          className="btn btn-ghost btn-sm"
          style={{ color: 'var(--coral-600)', fontSize: '0.78rem' }}
        >
          🚩 Report
        </button>
      </div>

      {/* Replies Section */}
      {showReplies && (
        <div style={{ marginTop: '16px', paddingTop: '14px', borderTop: '1px dashed var(--border-subtle)' }}>
          {post.replies?.map((rep) => (
            <div
              key={rep.id}
              style={{
                background: rep.isVerified ? 'var(--primary-50)' : 'var(--bg-subtle)',
                borderLeft: rep.isVerified ? '3px solid var(--primary-600)' : '2px solid var(--border-subtle)',
                padding: '12px 16px',
                borderRadius: '0 8px 8px 0',
                marginBottom: '10px'
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px' }}>
                <span style={{ fontSize: '0.8rem', fontWeight: 700, color: rep.isVerified ? 'var(--primary-800)' : 'var(--text-primary)' }}>
                  {rep.author}
                </span>
                {rep.isVerified && (
                  <span className="badge badge-success" style={{ fontSize: '0.68rem', padding: '1px 6px' }}>
                    ✓ Verified Educator
                  </span>
                )}
                <span style={{ fontSize: '0.7rem', color: 'var(--text-light)', marginLeft: 'auto' }}>
                  {formatDisplayDate(rep.date)}
                </span>
              </div>
              <p style={{ fontSize: '0.86rem', color: 'var(--text-secondary)', lineHeight: 1.5 }}>
                {rep.text}
              </p>
            </div>
          ))}

          {/* Quick Reply Form */}
          <form onSubmit={handleReplySubmit} style={{ display: 'flex', gap: '8px', marginTop: '12px' }}>
            <input
              type="text"
              placeholder="Add an educational or supportive comment..."
              value={replyText}
              onChange={(e) => setReplyText(e.target.value)}
              style={{ flex: 1, padding: '8px 12px', fontSize: '0.85rem' }}
            />
            <button type="submit" className="btn btn-primary btn-sm">
              Reply
            </button>
          </form>
        </div>
      )}
    </div>
  );
}
