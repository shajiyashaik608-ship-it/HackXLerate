import React, { useState } from 'react';
import PageHeader from '../components/PageHeader';
import CreatePost from '../features/community/CreatePost';
import PostFeed from '../features/community/PostFeed';
import ReportPostModal from '../features/community/ReportPostModal';

export default function Community({ posts, setPosts, language }) {
  const [activeReportPost, setActiveReportPost] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedTag, setSelectedTag] = useState('all');
  const [reportFeedback, setReportFeedback] = useState('');

  const isTelugu = language === 'te';

  const handleAddPost = (newPost) => {
    setPosts([newPost, ...posts]);
  };

  const handleVoteHelpful = (id) => {
    setPosts(
      posts.map((p) => {
        if (p.id === id) {
          return {
            ...p,
            helpfulCount: p.userVoted ? p.helpfulCount - 1 : p.helpfulCount + 1,
            userVoted: !p.userVoted
          };
        }
        return p;
      })
    );
  };

  const handleAddReply = (postId, replyText) => {
    const newReply = {
      id: `rep-${Date.now()}`,
      author: 'Priya S.',
      isVerified: false,
      date: new Date().toISOString().split('T')[0],
      text: replyText.trim()
    };

    setPosts(
      posts.map((p) =>
        p.id === postId ? { ...p, replies: [...(p.replies || []), newReply] } : p
      )
    );
  };

  const handleConfirmReport = (postId, reason) => {
    setPosts(
      posts.map((p) =>
        p.id === postId ? { ...p, isReported: true } : p
      )
    );
    setReportFeedback('Post flagged for clinical misinformation moderation review (Demo mode).');
    setActiveReportPost(null);
    setTimeout(() => setReportFeedback(''), 3500);
  };

  const filteredPosts = posts.filter((p) => {
    const matchesSearch =
      p.title?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      p.content?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      (p.tags && p.tags.some(t => t.toLowerCase().includes(searchQuery.toLowerCase())));

    const matchesTag =
      selectedTag === 'all' ||
      (p.tags && p.tags.some(t => t.toLowerCase().includes(selectedTag.toLowerCase())));

    return matchesSearch && matchesTag;
  });

  return (
    <div>
      <PageHeader
        title={isTelugu ? 'సురక్షిత PCOS కమ్యూనిటీ' : 'Safe PCOS Educational Community'}
        subtitle={isTelugu
          ? 'అనామక ప్రశ్నలు అడగండి, తోటివారి అనుభవాలు మరియు ధృవీకరించబడిన వైద్య విద్యావేత్తల సమాధానాలను చదవండి.'
          : 'A moderated educational discussion space where individuals exchange experiences and access clinician-reviewed guidance anonymously.'}
        badge="Moderated Peer Q&A"
      />

      {reportFeedback && (
        <div style={{
          background: 'var(--accent-yellow-light)',
          color: '#854d0e',
          padding: '10px 16px',
          borderRadius: 'var(--radius-md)',
          marginBottom: '16px',
          fontWeight: 500,
          border: '1px solid var(--accent-yellow)'
        }}>
          🛡️ {reportFeedback}
        </div>
      )}

      {/* Safety Notice */}
      <div style={{
        background: 'var(--primary-50)',
        border: '1px solid var(--primary-200)',
        borderRadius: 'var(--radius-md)',
        padding: '12px 18px',
        marginBottom: '20px',
        fontSize: '0.82rem',
        color: 'var(--primary-900)',
        display: 'flex',
        alignItems: 'center',
        gap: '10px'
      }}>
        <span style={{ fontSize: '1.2rem' }}>🔒</span>
        <span>
          <strong>Community Guidelines:</strong> All participation uses anonymous pseudonyms by default. Please do not share private addresses, phone numbers, or unredacted prescription documents. Unverified claims of "guaranteed cures" are prohibited.
        </span>
      </div>

      {/* Filter and Search Bar */}
      <div style={{ display: 'flex', gap: '10px', marginBottom: '20px', flexWrap: 'wrap' }}>
        <input
          type="text"
          placeholder="Search questions or topics (e.g. Inositol, Pesarattu, Flow)..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          style={{ flex: 1, minWidth: '220px', fontSize: '0.85rem' }}
        />
        <select
          value={selectedTag}
          onChange={(e) => setSelectedTag(e.target.value)}
          style={{ fontSize: '0.85rem', padding: '8px 12px' }}
        >
          <option value="all">All Topics</option>
          <option value="nutrition">Nutrition & Diet</option>
          <option value="cycle">Cycle & Symptoms</option>
          <option value="blood">Lab Reports</option>
          <option value="supplement">Supplements</option>
        </select>
      </div>

      <div className="grid-2" style={{ alignItems: 'flex-start' }}>
        <CreatePost onAddPost={handleAddPost} />

        <PostFeed
          posts={filteredPosts}
          onVoteHelpful={handleVoteHelpful}
          onAddReply={handleAddReply}
          onReport={setActiveReportPost}
        />
      </div>

      {/* Misinformation Reporting Modal */}
      <ReportPostModal
        post={activeReportPost}
        isOpen={Boolean(activeReportPost)}
        onClose={() => setActiveReportPost(null)}
        onConfirm={handleConfirmReport}
      />
    </div>
  );
}
