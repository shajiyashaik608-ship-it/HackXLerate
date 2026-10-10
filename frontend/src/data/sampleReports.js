export const SAMPLE_REPORTS = [
  {
    id: 'rep-1',
    fileName: 'Thyroid_and_Insulin_Panel_Oct2026.pdf',
    category: 'Blood Test',
    uploadDate: '2026-10-02',
    fileType: 'PDF',
    doctorNotes: 'Ordered by Dr. Sharmila (Gynecologist) to evaluate cycle delays and metabolic health.',
    biomarkers: [
      {
        testName: 'TSH (Thyroid Stimulating Hormone)',
        value: '4.85',
        unit: 'mIU/L',
        referenceRange: '0.40 - 4.50 mIU/L',
        status: 'elevated',
        plainExplanation: 'TSH is mildly elevated above the laboratory cut-off. High TSH indicates an underactive thyroid (subclinical hypothyroidism), which can directly disrupt ovulation and cycle frequency.'
      },
      {
        testName: 'Fasting Serum Insulin',
        value: '18.4',
        unit: 'uIU/mL',
        referenceRange: '2.0 - 24.9 uIU/mL',
        status: 'normal',
        plainExplanation: 'Within standard limits, but in the upper tier. In PCOS, clinicians monitor insulin levels to assess if dietary insulin resistance is contributing to androgen surges.'
      },
      {
        testName: 'HbA1c (Glycated Hemoglobin)',
        value: '5.3',
        unit: '%',
        referenceRange: '4.0 - 5.6 %',
        status: 'normal',
        plainExplanation: 'Healthy average blood glucose over the previous 90 days. Indicates good long-term glycemic management.'
      }
    ],
    plainSummary: 'Your panel highlights 1 borderline elevated biomarker (TSH at 4.85 mIU/L). Fasting insulin and HbA1c are within standard laboratory limits. This report is automatically cross-referenced in your Doctor Consultation Sheet.'
  },
  {
    id: 'rep-2',
    fileName: 'Pelvic_Ultrasound_Summary_Sep2026.pdf',
    category: 'Ultrasound',
    uploadDate: '2026-09-18',
    fileType: 'PDF',
    doctorNotes: 'Transvaginal sonography for ovarian volume and follicular monitoring.',
    biomarkers: [
      {
        testName: 'Right Ovarian Volume',
        value: '11.8',
        unit: 'cm³',
        referenceRange: '3.0 - 10.0 cm³',
        status: 'elevated',
        plainExplanation: 'Mildly increased volume. In PCOS, ovaries frequently appear mildly enlarged due to non-dominant follicles.'
      },
      {
        testName: 'Antral Follicle Count (Per Ovary)',
        value: '14 - 16',
        unit: 'follicles',
        referenceRange: '< 12 follicles',
        status: 'elevated',
        plainExplanation: 'Multiple immature follicles arranged peripherally (often described as "pearl necklace pattern"). Clinicians combine this with menstrual history for evaluation.'
      },
      {
        testName: 'Endometrial Thickness',
        value: '7.2',
        unit: 'mm',
        referenceRange: '4.0 - 12.0 mm',
        status: 'normal',
        plainExplanation: 'Normal uterine lining thickness for the post-menstrual phase.'
      }
    ],
    plainSummary: 'Pelvic ultrasound shows mild bilateral ovarian enlargement with peripheral follicles (14-16 follicles noted). Uterine architecture and endometrial stripe appear healthy.'
  }
];
