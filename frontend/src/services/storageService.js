/**
 * Storage service for managing demo browser localStorage persistence,
 * JSON data export, import, and storage telemetry.
 */

export const STORAGE_KEYS = {
  LANGUAGE: 'pcos_saathi_lang',
  PROFILE: 'pcos_saathi_profile',
  CYCLE_LOGS: 'pcos_saathi_cycle_logs',
  REPORTS: 'pcos_saathi_reports',
  REMINDERS: 'pcos_saathi_reminders',
  POSTS: 'pcos_saathi_posts',
  MEAL_PLAN: 'pcos_saathi_meal_plan',
  NOTIFS: 'pcos_saathi_notifs',
  CHAT: 'pcos_saathi_chat_history',
  ONBOARDING_COMPLETED: 'pcos_saathi_onboarding_completed',
  AUTH_USER: 'pcos_saathi_demo_user'
};

export const storageService = {
  /**
   * Calculates approximate size of all PCOS Saathi keys in localStorage
   */
  getStorageUsage: () => {
    let totalBytes = 0;
    try {
      Object.values(STORAGE_KEYS).forEach((key) => {
        const item = window.localStorage.getItem(key);
        if (item) {
          totalBytes += (key.length + item.length) * 2; // ~2 bytes per character
        }
      });
    } catch (e) {
      console.warn('Storage calculation error:', e);
    }
    const kb = (totalBytes / 1024).toFixed(2);
    return { bytes: totalBytes, kb, label: `${kb} KB` };
  },

  /**
   * Exports all user records into a downloadable JSON file
   */
  exportHealthData: () => {
    try {
      const exportObject = {
        app: 'Health Saathi (PCOS Saathi)',
        version: '1.0.0-hackathon',
        exportedAt: new Date().toISOString(),
        disclaimer: 'Educational demonstration records stored locally in browser sandbox.',
        data: {}
      };

      Object.entries(STORAGE_KEYS).forEach(([name, key]) => {
        const raw = window.localStorage.getItem(key);
        if (raw) {
          try {
            exportObject.data[name] = JSON.parse(raw);
          } catch {
            exportObject.data[name] = raw;
          }
        }
      });

      const dataStr = 'data:text/json;charset=utf-8,' + encodeURIComponent(JSON.stringify(exportObject, null, 2));
      const downloadAnchor = document.createElement('a');
      downloadAnchor.setAttribute('href', dataStr);
      downloadAnchor.setAttribute('download', `health_saathi_backup_${new Date().toISOString().split('T')[0]}.json`);
      document.body.appendChild(downloadAnchor);
      downloadAnchor.click();
      downloadAnchor.remove();
      return true;
    } catch (error) {
      console.error('Export failed:', error);
      return false;
    }
  },

  /**
   * Imports previously exported JSON data
   */
  importHealthData: (jsonString) => {
    try {
      const parsed = JSON.parse(jsonString);
      if (!parsed || !parsed.data) {
        throw new Error('Invalid Health Saathi backup format.');
      }

      Object.entries(STORAGE_KEYS).forEach(([name, key]) => {
        if (parsed.data[name] !== undefined) {
          const value = typeof parsed.data[name] === 'object'
            ? JSON.stringify(parsed.data[name])
            : parsed.data[name];
          window.localStorage.setItem(key, value);
        }
      });
      return { success: true };
    } catch (err) {
      return { success: false, error: err.message };
    }
  },

  /**
   * Granularly clears a specific storage category
   */
  clearCategory: (key) => {
    try {
      window.localStorage.removeItem(key);
      return true;
    } catch {
      return false;
    }
  }
};
