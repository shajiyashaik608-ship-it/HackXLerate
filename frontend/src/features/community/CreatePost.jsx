import React, { useState } from 'react';

export default function CreatePost({ onAddPost }) {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [category, setCategory] = useState('Nutrition');
  const [isAnonymous, setIsAnonymous] = useState(true);

  const categories = [
    'PCOS Education',
    'Nutrition',
    'Menstrual Health',
    'Emotional Wellbeing',
    'Doctor Visit Questions',
    'Lifestyle Experiences'
  ];

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!title.trim() || !content.trim()) return;

    const newPost = {
      id: `post-${Date.now()}`,
      author: isAnonymous ? `Anonymous Saathi #${Math.floor(100 + Math.random() * 900)}` : 'Priya S.',
      category,
      title: title.trim(),
      content: content.trim(),
      date: new Date().toISOString().split('T')[0],
      helpfulCount: 0,
      userVoted: false,
      replies: []
    };

    onAddPost(newPost);
    setTitle('');
    setContent('');
  };

  return (
    <div className="card" style={{ marginBottom: '24px' }}>
      <h3 style={{ fontSize: '1.15rem', color: 'var(--text-primary)', marginBottom: '6px' }}>
        💬 Ask or Share with Safe Community
      </h3>
      <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)', marginBottom: '14px' }}>
        Posts are public to the local demo board. Never share private phone numbers, home addresses, or hospital ID cards.
      </p>

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label className="form-label">Discussion Title / Question *</label>
          <input
            type="text"
            placeholder="e.g., How do you navigate breakfast when traveling?"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
          />
        </div>

        <div className="grid-2">
          <div className="form-group">
            <label className="form-label">Topic Category</label>
            <select value={category} onChange={(e) => setCategory(e.target.value)}>
              {categories.map((c) => (
                <option key={c} value={c}>{c}</option>
              ))}
            </select>
          </div>

          <div className="form-group" style={{ justifyContent: 'center' }}>
            <label style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer', fontSize: '0.85rem', color: 'var(--text-secondary)', marginTop: '20px' }}>
              <input
                type="checkbox"
                checked={isAnonymous}
                onChange={(e) => setIsAnonymous(e.target.checked)}
                style={{ accentColor: 'var(--primary-700)' }}
              />
              🔒 Post with Anonymous Pseudonym
            </label>
          </div>
        </div>

        <div className="form-group">
          <label className="form-label">Details / Lived Experience *</label>
          <textarea
            rows="3"
            placeholder="Share your question or supportive tip here..."
            value={content}
            onChange={(e) => setContent(e.target.value)}
            required
          />
        </div>

        <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
          <button type="submit" className="btn btn-primary">
            Publish Question
          </button>
        </div>
      </form>
    </div>
  );
}
