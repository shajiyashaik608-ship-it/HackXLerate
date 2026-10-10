import React, { useState } from 'react';
import PageHeader from '../components/PageHeader';
import FormField from '../components/FormField';
import ConfirmDialog from '../components/ConfirmDialog';
import { validateName, validateAge, validateCycleLength } from '../utils/validation';

export default function HealthProfile({ profile, setProfile, language, setLanguage }) {
  const [formData, setFormData] = useState({ ...profile });
  const [errors, setErrors] = useState({});
  const [savedSuccess, setSavedSuccess] = useState(false);
  const [showResetConfirm, setShowResetConfirm] = useState(false);

  const isTelugu = language === 'te';

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: '' }));
    }
  };

  const handleSave = (e) => {
    e.preventDefault();

    const newErrors = {};
    const nameErr = validateName(formData.name);
    if (nameErr) newErrors.name = nameErr;

    const ageErr = validateAge(formData.age);
    if (ageErr) newErrors.age = ageErr;

    const cycleErr = validateCycleLength(formData.cycleLength);
    if (cycleErr) newErrors.cycleLength = cycleErr;

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    setProfile(formData);
    if (formData.language) {
      setLanguage(formData.language);
    }
    setSavedSuccess(true);
    setTimeout(() => setSavedSuccess(false), 2500);
  };

  const confirmResetProfile = () => {
    const defaultProfile = {
      name: 'Priya Sharma',
      age: 24,
      language: 'en',
      dietType: 'vegetarian',
      allergies: 'None',
      cycleLength: 33,
      periodDuration: 4,
      wellnessGoals: 'Manage insulin resistance and establish predictable menstrual cycles.'
    };
    setFormData(defaultProfile);
    setProfile(defaultProfile);
    setShowResetConfirm(false);
    setSavedSuccess(true);
    setTimeout(() => setSavedSuccess(false), 2500);
  };

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto' }}>
      <PageHeader
        title={isTelugu ? 'నా ఆరోగ్య ప్రొఫైల్' : 'My Health Profile'}
        subtitle={isTelugu
          ? 'మీ వ్యక్తిగత ప్రాధాన్యతలు, ఆహార అలవాట్లు మరియు సైకిల్ వివరాలను నిర్వహించండి.'
          : 'Customize your personal preferences, dietary restrictions, and typical cycle parameters for tailored guidance.'}
        badge="Personal Settings"
        actions={
          <button onClick={() => setShowResetConfirm(true)} className="btn btn-outline btn-sm">
            Reset Demo Profile
          </button>
        }
      />

      {savedSuccess && (
        <div style={{
          background: 'var(--accent-green-light)',
          color: '#166534',
          padding: '12px 18px',
          borderRadius: 'var(--radius-md)',
          marginBottom: '20px',
          fontWeight: 600,
          border: '1px solid var(--accent-green)'
        }}>
          ✓ Health profile preferences saved successfully.
        </div>
      )}

      <form onSubmit={handleSave} className="card">
        <h3 style={{ fontSize: '1.2rem', color: 'var(--text-primary)', marginBottom: '18px' }}>
          Biometric & Linguistic Preferences
        </h3>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', marginBottom: '16px' }}>
          <FormField
            label="Full Name"
            id="prof-name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            error={errors.name}
            required
          />

          <FormField
            label="Age (Years)"
            id="prof-age"
            name="age"
            type="number"
            value={formData.age}
            onChange={handleChange}
            error={errors.age}
            required
          />
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', marginBottom: '16px' }}>
          <div className="form-group">
            <label className="form-label" style={{ display: 'block', fontSize: '0.84rem', fontWeight: 600, marginBottom: '6px' }}>
              Dietary Lifestyle Preference
            </label>
            <select
              name="dietType"
              value={formData.dietType}
              onChange={handleChange}
              style={{ width: '100%' }}
            >
              <option value="vegetarian">Vegetarian (Lacto-Vegetarian)</option>
              <option value="egg">Eggetarian (Includes eggs)</option>
              <option value="all">Non-Vegetarian (Includes fish/poultry)</option>
            </select>
          </div>

          <FormField
            label="Allergies / Intolerances"
            id="prof-allergies"
            name="allergies"
            value={formData.allergies}
            onChange={handleChange}
            placeholder="e.g. Gluten, Dairy, Peanut"
          />
        </div>

        <h3 style={{ fontSize: '1.2rem', color: 'var(--text-primary)', margin: '24px 0 16px 0' }}>
          Menstrual Rhythm Baseline
        </h3>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', marginBottom: '16px' }}>
          <FormField
            label="Baseline Cycle Interval (Days)"
            id="prof-cycle"
            name="cycleLength"
            type="number"
            value={formData.cycleLength}
            onChange={handleChange}
            error={errors.cycleLength}
            hint="Natural PCOS range typically 30-45 days"
            required
          />

          <FormField
            label="Typical Period Duration (Days)"
            id="prof-duration"
            name="periodDuration"
            type="number"
            value={formData.periodDuration}
            onChange={handleChange}
            hint="Days of active menstrual flow"
          />
        </div>

        <FormField
          label="Primary Wellness Target"
          id="prof-goals"
          name="wellnessGoals"
          value={formData.wellnessGoals}
          onChange={handleChange}
          placeholder="e.g. Reduce insulin resistance, stabilize acne, improve cycle regularity"
        />

        <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '12px', marginTop: '24px' }}>
          <button type="submit" className="btn btn-primary">
            Save Profile Changes
          </button>
        </div>
      </form>

      {/* Reset Confirmation */}
      <ConfirmDialog
        isOpen={showResetConfirm}
        title="Reset Demo Profile"
        message="Reset all profile parameters back to the default demo persona (Priya Sharma, Age 24)?"
        confirmLabel="Reset Profile"
        isDestructive={true}
        onConfirm={confirmResetProfile}
        onCancel={() => setShowResetConfirm(false)}
      />
    </div>
  );
}
