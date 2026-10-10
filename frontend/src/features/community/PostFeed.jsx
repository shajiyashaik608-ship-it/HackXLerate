import React, { useState } from 'react';
import CommunityPost from '../../components/CommunityPost';
import EmptyState from '../../components/EmptyState';

export default function PostFeed({
  posts,
  onVoteHelpful,
  onAddReply,
  onReport
}) {
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [searchTerm, setSearchTerm] = useState('');

  const categories = [
    'All',
    'Nutrition',
    'Menstrual Health',
    'Doctor Visit Questions',
    'PCOS Education',
    'Emotional Wellbeing'
  ];

  const filteredPosts = posts.filter((post) => {
    const matchesCategory = selectedCategory === 'All' || post.category === selectedCategory;
    const matchesSearch =
      post.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      post.content.toLowerCase().includes(searchTerm.toLowerCase());
    return matchesCategory && matchesSearch;
  });

  return (
    <div>
      {/* Search and Category Filters */}
      <div className="card" style={{ padding: '16px 20px', marginBottom: '20px' }}>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '14px', alignItems: 'center', justifyContent: 'space-between' }}>
          <div style={{ flex: '1 1 260px' }}>
            <input
              type="text"
              placeholder="Search community discussions..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              style={{ width: '100%', borderRadius: 'var(--radius-full)', padding: '8px 16px', fontSize: '0.86rem' }}
            />
          </div>

          <div style={{ display: 'flex', gap: '6px', overflowX: 'auto', padding: '2px 0' }}>
            {categories.map((cat) => (
              <button
                key={cat}
                onClick={() => setSelectedCategory(cat)}
                className={`btn btn-sm ${selectedCategory === cat ? 'btn-primary' : 'btn-outline'}`}
                style={{ borderRadius: 'var(--radius-full)' }}
              >
                {cat}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Feed List */}
      {filteredPosts.length === 0 ? (
        <EmptyState
          icon="💬"
          title="No discussions match your filter"
          description="Try selecting a different topic category or clearing your search keywords."
        />
      ) : (
        filteredPosts.map((post) => (
          <CommunityPost
            key={post.id}
            post={post}
            onVoteHelpful={onVoteHelpful}
            onAddReply={onAddReply}
            onReport={onReport}
          />
        ))
      )}
    </div>
  );
}
