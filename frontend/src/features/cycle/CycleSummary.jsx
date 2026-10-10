import React from 'react';
import { formatDisplayDate, estimateNextPeriod, calculateCyclePhase } from '../../utils/dateUtils';

export default function CycleSummary({ cycleLogs, avgCycleLength = 33 }) {
  const latestLog = cycleLogs.length > 0 ? cycleLogs[0] : null;
  const estimate = latestLog ? estimateNextPeriod(latestLog.startDate, avgCycleLength) : null;
  const phaseInfo = latestLog ? calculateCyclePhase(latestLog.startDate, avgCycleLength) : null;

  return (
    <div className="grid-3" style={{ marginBottom: '24px' }}>
      {/* Card 1: Current Estimated Phase */}
      <div className="card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '8px' }}>
          <span style={{ fontSize: '1.4rem' }}>🌸</span>
          <span className="badge badge-lavender">
            Day {phaseInfo ? phaseInfo.dayNumber : 0} of Cycle
          </span>
        </div>
        <div style={{ fontSize: '0.82rem', color: 'var(--text-muted)', fontWeight: 600, textTransform: 'uppercase' }}>
          Current Phase Estimate
        </div>
        <div style={{ fontSize: '1.35rem', fontWeight: 700, color: 'var(--text-primary)', marginTop: '4px' }}>
          {phaseInfo ? phaseInfo.phaseName : 'Awaiting Period Log'}
        </div>
        <div style={{ fontSize: '0.78rem', color: 'var(--text-secondary)', marginTop: '6px' }}>
          Based on typical {avgCycleLength}-day cycle interval.
        </div>
      </div>

      {/* Card 2: Next Window Prediction */}
      <div className="card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '8px' }}>
          <span style={{ fontSize: '1.4rem' }}>⏱️</span>
          <span className="badge badge-warning">Cautious Window</span>
        </div>
        <div style={{ fontSize: '0.82rem', color: 'var(--text-muted)', fontWeight: 600, textTransform: 'uppercase' }}>
          Estimated Next Period
        </div>
        <div style={{ fontSize: '1.35rem', fontWeight: 700, color: 'var(--primary-700)', marginTop: '4px' }}>
          {estimate ? estimate.windowRange : 'Log cycle to calculate'}
        </div>
        <div style={{ fontSize: '0.78rem', color: '#854d0e', marginTop: '6px' }}>
          {estimate ? estimate.varianceText : 'PCOS cycles naturally vary.'}
        </div>
      </div>

      {/* Card 3: Historical Overview */}
      <div className="card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '8px' }}>
          <span style={{ fontSize: '1.4rem' }}>📊</span>
          <span className="badge badge-primary">{cycleLogs.length} Cycles Logged</span>
        </div>
        <div style={{ fontSize: '0.82rem', color: 'var(--text-muted)', fontWeight: 600, textTransform: 'uppercase' }}>
          Last Recorded Cycle
        </div>
        <div style={{ fontSize: '1.35rem', fontWeight: 700, color: 'var(--text-primary)', marginTop: '4px' }}>
          {latestLog ? formatDisplayDate(latestLog.startDate) : 'None'}
        </div>
        <div style={{ fontSize: '0.78rem', color: 'var(--text-secondary)', marginTop: '6px' }}>
          Flow: {latestLog?.flow || 'N/A'} • Duration: {latestLog?.durationDays || 4} days
        </div>
      </div>
    </div>
  );
}
