/**
 * Validation utilities for Health Saathi frontend
 */

export const validateName = (name) => {
  if (!name || !name.trim()) return 'Name is required.';
  if (name.trim().length < 2) return 'Name must be at least 2 characters.';
  if (name.trim().length > 50) return 'Name must be under 50 characters.';
  return '';
};

export const validateAge = (age) => {
  const num = Number(age);
  if (!age || isNaN(num)) return 'Age is required and must be a number.';
  if (num < 12 || num > 90) return 'Age must be between 12 and 90.';
  return '';
};

export const validateCycleLength = (length) => {
  const num = Number(length);
  if (!length || isNaN(num)) return 'Cycle length is required.';
  if (num < 20 || num > 90) return 'Expected cycle length is typically between 20 and 90 days.';
  return '';
};

export const validateFile = (file, maxSizeMB = 10) => {
  if (!file) return 'Please select a document.';
  const allowedExtensions = ['.pdf', '.jpg', '.jpeg', '.png'];
  const ext = file.name.substring(file.name.lastIndexOf('.')).toLowerCase();
  
  if (!allowedExtensions.includes(ext)) {
    return 'Invalid file format. Only PDF, JPG, and PNG files are supported.';
  }

  const maxSizeBytes = maxSizeMB * 1024 * 1024;
  if (file.size > maxSizeBytes) {
    return `File size exceeds the ${maxSizeMB}MB limit. Please upload a smaller file.`;
  }

  return '';
};

export const validateReminder = (title, time) => {
  const errors = {};
  if (!title || !title.trim()) {
    errors.title = 'Reminder title is required.';
  }
  if (!time) {
    errors.time = 'Reminder time is required.';
  }
  return errors;
};
