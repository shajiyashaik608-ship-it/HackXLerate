import React, { useState } from 'react';

export default function CommunityQA({ language }) {
  const [posts, setPosts] = useState([
    {
      id: 1,
      author: "Anonymous Saathi",
      tag: "nutrition",
      title: "Best ways to manage dairy cravings with South Indian breakfast?",
      content: "I used to have tea with cow milk and curd every morning. What are good substitutes that support insulin levels?",
      answers: [
        {
          author: "Dr. Ananya R. (Verified Clinical Educator)",
          badge: "Doctor Reviewed",
          text: "Fermented probiotic curd in small portions typically has lower lactose. For tea, almond milk or oat milk without added cane sugar provides a gentler glucose curve. Pairing with moong dal pesarattu stabilizes morning energy."
        }
      ]
    },
    {
      id: 2,
      author: "Sunitha K.",
      tag: "lifestyle",
      title: "పీరియడ్స్ ఆలస్యం అయినప్పుడు ఎలాంటి యోగాసనాలు మేలు చేస్తాయి?",
      content: "PCOS లో సహజంగా పీరియడ్స్ క్రమబద్ధం కావడానికి బటర్‌ఫ్లై పోజ్ (Baddha Konasana) పనికొస్తుందా?",
      answers: [
        {
          author: "Health Saathi Team",
          badge: "Educator Response",
          text: "అవును, బద్ధకోణాసనం మరియు సుప్త బద్ధకోణాసనం పెల్విక్ ప్రాంతంలో రక్తప్రసరణను మెరుగుపరుస్తాయి. రోజుకు 15 నిమిషాలు సాధన చేయడం ప్రయోజనకరం."
        }
      ]
    }
  ]);

  const [newTitle, setNewTitle] = useState('');
  const [newContent, setNewContent] = useState('');
  const [isAnonymous, setIsAnonymous] = useState(true);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!newTitle.trim()) return;

    const newPost = {
      id: Date.now(),
      author: isAnonymous ? "Anonymous Saathi" : "Priya S.",
      tag: "lifestyle",
      title: newTitle,
      content: newContent,
      answers: []
    };

    setPosts([newPost, ...posts]);
    setNewTitle('');
    setNewContent('');
  };

  return (
    <div style={{ maxWidth: '1000px', margin: '0 auto', padding: '24px 20px' }}>
      <div style={{ marginBottom: '24px' }}>
        <h1 style={{ fontSize: '1.8rem', color: '#0f172a', marginBottom: '6px' }}>
          💬 Safe PCOS Community (Educational Q&A)
        </h1>
        <p style={{ color: '#64748b', fontSize: '0.95rem' }}>
          A moderated, safe space to ask questions, share shared journeys, and receive responses reviewed by verified health educators.
        </p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1.2fr 2fr', gap: '24px' }}>
        {/* Post Form */}
        <div>
          <div className="glass-panel" style={{ padding: '22px' }}>
            <h3 style={{ fontSize: '1.1rem', marginBottom: '14px', color: '#0f172a' }}>Ask an Educational Question</h3>
            <form onSubmit={handleSubmit}>
              <div style={{ marginBottom: '12px' }}>
                <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, marginBottom: '4px' }}>
                  Question Title
                </label>
                <input
                  type="text"
                  placeholder="e.g., How to handle evening fatigue?"
                  value={newTitle}
                  onChange={(e) => setNewTitle(e.target.value)}
                  style={{
                    width: '100%',
                    padding: '8px 12px',
                    borderRadius: '8px',
                    border: '1px solid #cbd5e1',
                    fontSize: '0.88rem'
                  }}
                />
              </div>

              <div style={{ marginBottom: '14px' }}>
                <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, marginBottom: '4px' }}>
                  Context / Details
                </label>
                <textarea
                  rows="3"
                  placeholder="Describe your question or lived experience..."
                  value={newContent}
                  onChange={(e) => setNewContent(e.target.value)}
                  style={{
                    width: '100%',
                    padding: '8px 12px',
                    borderRadius: '8px',
                    border: '1px solid #cbd5e1',
                    fontSize: '0.85rem'
                  }}
                ></textarea>
              </div>

              <div style={{ marginBottom: '16px' }}>
                <label style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.82rem', color: '#475569', cursor: 'pointer' }}>
                  <input
                    type="checkbox"
                    checked={isAnonymous}
                    onChange={(e) => setIsAnonymous(e.target.checked)}
                  />
                  🔒 Post anonymously (as Anonymous Saathi)
                </label>
              </div>

              <button type="submit" className="btn-primary" style={{ width: '100%', justifyContent: 'center' }}>
                Submit to Moderated Q&A
              </button>
            </form>
          </div>
        </div>

        {/* Posts List */}
        <div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            {posts.map((post) => (
              <div key={post.id} className="glass-panel" style={{ padding: '22px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                  <span style={{ fontSize: '0.78rem', color: '#64748b' }}>
                    Asked by <strong>{post.author}</strong>
                  </span>
                  <span className="badge badge-normal" style={{ fontSize: '0.7rem' }}>
                    #{post.tag}
                  </span>
                </div>

                <h3 style={{ fontSize: '1.05rem', color: '#0f172a', marginBottom: '6px' }}>
                  {post.title}
                </h3>
                <p style={{ fontSize: '0.88rem', color: '#475569', marginBottom: '14px', lineHeight: '1.5' }}>
                  {post.content}
                </p>

                {/* Answers Section */}
                {post.answers.length > 0 ? (
                  <div style={{
                    background: '#f8fafc',
                    borderLeft: '3px solid #0f766e',
                    padding: '12px 14px',
                    borderRadius: '0 8px 8px 0'
                  }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px' }}>
                      <span style={{ fontWeight: 600, fontSize: '0.8rem', color: '#0f766e' }}>
                        {post.answers[0].author}
                      </span>
                      <span style={{
                        background: '#d1fae5',
                        color: '#065f46',
                        fontSize: '0.68rem',
                        padding: '1px 6px',
                        borderRadius: '4px',
                        fontWeight: 600
                      }}>
                        {post.answers[0].badge}
                      </span>
                    </div>
                    <p style={{ fontSize: '0.84rem', color: '#334155', lineHeight: '1.5' }}>
                      {post.answers[0].text}
                    </p>
                  </div>
                ) : (
                  <div style={{ fontSize: '0.78rem', color: '#94a3b8', fontStyle: 'italic' }}>
                    ⏳ Awaiting verified educator review...
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
