import React, { useState } from 'react';
import PageHeader from '../components/PageHeader';
import ReportCard from '../components/ReportCard';
import UploadPanel from '../features/reports/UploadPanel';
import ReportSummary from '../features/reports/ReportSummary';
import ConfirmDialog from '../components/ConfirmDialog';

export default function MedicalReports({ reports, setReports, language }) {
  const [activeReport, setActiveReport] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [reportToDelete, setReportToDelete] = useState(null);

  const isTelugu = language === 'te';

  const handleAddReport = (newRep) => {
    setReports([newRep, ...reports]);
  };

  const handleUpdateReport = (updatedRep) => {
    setReports(reports.map((r) => (r.id === updatedRep.id ? updatedRep : r)));
    setActiveReport(updatedRep);
  };

  const confirmDeleteReport = () => {
    if (reportToDelete) {
      setReports(reports.filter((r) => r.id !== reportToDelete.id));
      if (activeReport?.id === reportToDelete.id) setActiveReport(null);
      setReportToDelete(null);
    }
  };

  const filteredReports = reports.filter((rep) => {
    const matchesSearch =
      rep.fileName.toLowerCase().includes(searchQuery.toLowerCase()) ||
      rep.category.toLowerCase().includes(searchQuery.toLowerCase()) ||
      (rep.doctorNotes && rep.doctorNotes.toLowerCase().includes(searchQuery.toLowerCase()));

    const matchesCategory =
      selectedCategory === 'all' ||
      rep.category.toLowerCase().includes(selectedCategory.toLowerCase());

    return matchesSearch && matchesCategory;
  });

  return (
    <div>
      <PageHeader
        title={isTelugu ? 'వైద్య రికార్డులు & ప్రిస్క్రిప్షన్లు' : 'Medical Reports & Prescription Organizer'}
        subtitle={isTelugu
          ? 'మీ ల్యాబ్ పరీక్షలు, థైరాయిడ్ మరియు అల్ట్రాసౌండ్ రిపోర్టులను భద్రపరచండి. వైద్య పరిభాషను సాధారణ భాషలో అర్థం చేసుకోండి.'
          : 'Upload diagnostic panels, track biomarker reference ranges, and decode medical terminology for confident clinician consultations.'}
        badge="OCR Simulation Ready"
      />

      <div className="grid-2" style={{ alignItems: 'flex-start' }}>
        {/* Upload Column */}
        <UploadPanel onUploadSuccess={handleAddReport} />

        {/* Existing Reports Column */}
        <div>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '14px', flexWrap: 'wrap', gap: '10px' }}>
            <h3 style={{ fontSize: '1.15rem', color: 'var(--text-primary)', margin: 0 }}>
              📋 Stored Clinical Documents ({filteredReports.length})
            </h3>
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              style={{ fontSize: '0.8rem', padding: '6px 10px' }}
            >
              <option value="all">All Categories</option>
              <option value="thyroid">Thyroid Profile</option>
              <option value="metabolic">Metabolic & Insulin</option>
              <option value="hormon">Hormonal Profile</option>
              <option value="ultrasound">Pelvic Ultrasound</option>
            </select>
          </div>

          {/* Search Box */}
          <div style={{ marginBottom: '14px' }}>
            <input
              type="text"
              placeholder="Search reports by filename or biomarker..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              style={{ width: '100%', fontSize: '0.84rem' }}
            />
          </div>

          {filteredReports.length === 0 ? (
            <div className="card" style={{ textAlign: 'center', padding: '36px', color: 'var(--text-muted)', fontSize: '0.86rem' }}>
              No matching clinical reports found. Try clearing your search filter or upload a new record.
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
              {filteredReports.map((rep) => (
                <ReportCard
                  key={rep.id}
                  report={rep}
                  onView={setActiveReport}
                  onDelete={(id) => setReportToDelete(rep)}
                />
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Report Detail & Plain Language Explanation Modal */}
      <ReportSummary
        report={activeReport}
        isOpen={Boolean(activeReport)}
        onClose={() => setActiveReport(null)}
        onUpdateReport={handleUpdateReport}
      />

      {/* Accessible Delete Confirmation Dialog */}
      <ConfirmDialog
        isOpen={Boolean(reportToDelete)}
        title="Remove Medical Document"
        message={`Are you sure you want to remove "${reportToDelete?.fileName}" from your locally stored demo records? This action cannot be undone.`}
        confirmLabel="Remove Report"
        isDestructive={true}
        onConfirm={confirmDeleteReport}
        onCancel={() => setReportToDelete(null)}
      />
    </div>
  );
}
