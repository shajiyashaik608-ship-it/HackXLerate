import React from 'react';
import { formatDisplayDate } from '../utils/dateUtils';

export default function ReportCard({
  report,
  onView,
  onDelete
}) {
  const elevatedCount = report.biomarkers?.filter((b) => b.status === 'elevated').length || 0;

  return (
    <div className="card" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
      <div>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '12px' }}>
          <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
            <span style={{ fontSize: '1.5rem' }}>📄</span>
            <div>
              <span className="badge badge-primary">{report.category}</span>
              <span style={{ marginLeft: '6px', fontSize: '0.72rem', color: 'var(--text-light)', fontWeight: 600 }}>
                {report.fileType}
              </span>
            </div>
          </div>
          {elevatedCount > 0 ? (
            <span className="badge badge-coral">{elevatedCount} Flagged</span>
          ) : (
            <span className="badge badge-success">Normal Range</span>
          )}
        </div>

        <h3 style={{ fontSize: '1.05rem', color: 'var(--text-primary)', marginBottom: '6px', wordBreak: 'break-word' }}>
          {report.fileName}
        </h3>

        <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginBottom: '12px' }}>
          Uploaded on {formatDisplayDate(report.uploadDate)}
        </div>

        {report.doctorNotes && (
          <p style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', background: 'var(--bg-subtle)', padding: '8px 12px', borderRadius: '8px', marginBottom: '14px' }}>
            📝 {report.doctorNotes}
          </p>
        )}
      </div>

      <div style={{
        paddingTop: '12px',
        borderTop: '1px solid var(--border-subtle)',
        display: 'flex',
        justifyContent: 'space-between',
        gap: '8px'
      }}>
        <button onClick={() => onView(report)} className="btn btn-primary btn-sm" style={{ flex: 1 }}>
          View Analysis
        </button>
        {onDelete && (
          <button onClick={() => onDelete(report.id)} className="btn btn-outline btn-sm" title="Remove demo report">
            🗑️
          </button>
        )}
      </div>
    </div>
  );
}
