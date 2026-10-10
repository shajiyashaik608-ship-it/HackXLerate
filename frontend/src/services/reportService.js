/**
 * Report service providing simulated OCR document processing,
 * multi-stage extraction progress, biomarker parsing, and validation.
 */

export const OCR_STAGES = [
  { step: 1, name: 'Scanning document layout...', percent: 25 },
  { step: 2, name: 'Extracting text via optical recognition...', percent: 55 },
  { step: 3, name: 'Structuring clinical biomarker tables...', percent: 85 },
  { step: 4, name: 'Benchmarking physiological reference ranges...', percent: 100 }
];

export const DEMO_EXTRACTION_PRESETS = {
  'thyroid': {
    category: 'Thyroid Profile',
    biomarkers: [
      {
        testName: 'TSH (Thyroid Stimulating Hormone)',
        value: '4.85',
        unit: 'mIU/L',
        referenceRange: '0.40 - 4.20 mIU/L',
        status: 'elevated',
        isManualEdit: false,
        sourceDoc: 'Thyroid_Panel_Aug.pdf',
        plainExplanation: 'TSH is slightly high, indicating your pituitary gland is producing extra hormone to stimulate thyroid activity. Often correlated with delayed follicular development in PCOS.'
      },
      {
        testName: 'Free T4 (Thyroxine)',
        value: '1.18',
        unit: 'ng/dL',
        referenceRange: '0.80 - 1.80 ng/dL',
        status: 'normal',
        isManualEdit: false,
        sourceDoc: 'Thyroid_Panel_Aug.pdf',
        plainExplanation: 'Active thyroid hormone is circulating in healthy normal concentrations.'
      }
    ],
    plainSummary: 'Mildly elevated TSH detected. Subclinical hypothyroid patterns are common in PCOS and can be discussed during your consultation.'
  },
  'metabolic': {
    category: 'Metabolic & Insulin',
    biomarkers: [
      {
        testName: 'Fasting Insulin',
        value: '18.4',
        unit: 'µIU/mL',
        referenceRange: '2.6 - 12.0 µIU/mL',
        status: 'elevated',
        isManualEdit: false,
        sourceDoc: 'Metabolic_Panel.pdf',
        plainExplanation: 'Elevated fasting insulin is a classic indicator of peripheral insulin resistance. More insulin is needed to clear glucose from blood.'
      },
      {
        testName: 'Fasting Blood Glucose',
        value: '94',
        unit: 'mg/dL',
        referenceRange: '70 - 99 mg/dL',
        status: 'normal',
        isManualEdit: false,
        sourceDoc: 'Metabolic_Panel.pdf',
        plainExplanation: 'Blood glucose remains well controlled within standard normal ranges.'
      },
      {
        testName: 'HbA1c',
        value: '5.5',
        unit: '%',
        referenceRange: '< 5.7 %',
        status: 'normal',
        isManualEdit: false,
        sourceDoc: 'Metabolic_Panel.pdf',
        plainExplanation: 'Three-month average blood glucose level is in the healthy non-diabetic range.'
      }
    ],
    plainSummary: 'Fasting insulin shows mild elevation while glucose remains normal, reflecting early compensatory insulin resistance.'
  },
  'hormone': {
    category: 'Hormonal Profile',
    biomarkers: [
      {
        testName: 'Total Testosterone',
        value: '58',
        unit: 'ng/dL',
        referenceRange: '15 - 45 ng/dL',
        status: 'elevated',
        isManualEdit: false,
        sourceDoc: 'Hormone_Assay.pdf',
        plainExplanation: 'Elevated circulating androgen levels, which commonly contribute to cystic acne, hirsutism, or delayed ovulation.'
      },
      {
        testName: 'LH / FSH Ratio',
        value: '2.4:1',
        unit: 'ratio',
        referenceRange: '1:1 ratio',
        status: 'elevated',
        isManualEdit: false,
        sourceDoc: 'Hormone_Assay.pdf',
        plainExplanation: 'Luteinizing Hormone (LH) is higher relative to Follicle Stimulating Hormone (FSH), a standard clinical observation in PCOS.'
      }
    ],
    plainSummary: 'Androgen levels and LH/FSH ratio indicate hormonal variance typical of polycystic ovarian patterns.'
  }
};

export const reportService = {
  /**
   * Simulates step-by-step OCR extraction with progress callbacks
   */
  processDocument: async (file, onProgress) => {
    return new Promise((resolve, reject) => {
      let stageIndex = 0;

      const interval = setInterval(() => {
        if (stageIndex < OCR_STAGES.length) {
          const stage = OCR_STAGES[stageIndex];
          onProgress(stage);
          stageIndex++;
        } else {
          clearInterval(interval);
          
          // Match preset based on filename keywords
          const fileName = file.name.toLowerCase();
          let matched = DEMO_EXTRACTION_PRESETS.thyroid;
          if (fileName.includes('insulin') || fileName.includes('sugar') || fileName.includes('metabolic') || fileName.includes('glucose')) {
            matched = DEMO_EXTRACTION_PRESETS.metabolic;
          } else if (fileName.includes('hormone') || fileName.includes('pcos') || fileName.includes('testosterone') || fileName.includes('lh')) {
            matched = DEMO_EXTRACTION_PRESETS.hormone;
          }

          const result = {
            id: `rep-${Date.now()}`,
            fileName: file.name,
            fileType: file.name.endsWith('.pdf') ? 'PDF' : 'IMAGE',
            category: matched.category,
            uploadDate: new Date().toISOString().split('T')[0],
            isSimulatedExtraction: true,
            biomarkers: matched.biomarkers.map((b) => ({ ...b, sourceDoc: file.name })),
            plainSummary: matched.plainSummary,
            doctorNotes: 'Uploaded by patient for upcoming consultation review.'
          };

          resolve(result);
        }
      }, 350);
    });
  }
};
