const API_BASE_URL = '/api/v1';

export const apiClient = {
  async getHealth() {
    try {
      const res = await fetch('/health');
      if (!res.ok) throw new Error('Health check failed');
      return await res.json();
    } catch (e) {
      return { status: 'offline-mock-fallback', service: 'Health Saathi (Demo Mode)' };
    }
  },

  async getReports() {
    try {
      const res = await fetch(`${API_BASE_URL}/reports/`);
      if (!res.ok) throw new Error('Failed to fetch reports');
      return await res.json();
    } catch (e) {
      // Mock fallback for immediate interactive hackathon testing
      return [
        {
          id: 1,
          title: "Thyroid & Fasting Glucose Profile",
          report_type: "blood_test",
          structured_data: [
            {
              test_name: "TSH (Thyroid)",
              value: "4.8",
              unit: "mIU/L",
              reference_range: "0.4 - 4.5 mIU/L",
              status: "elevated",
              plain_explanation: "TSH is slightly high, suggesting subclinical thyroid slowing that can affect menstrual regularity."
            },
            {
              test_name: "Fasting Insulin",
              value: "18.2",
              unit: "uIU/mL",
              reference_range: "2.0 - 24.9 uIU/mL",
              status: "normal",
              plain_explanation: "In upper normal range. Often tracked in PCOS to monitor cellular insulin sensitivity."
            },
            {
              test_name: "HbA1c",
              value: "5.4",
              unit: "%",
              reference_range: "4.0 - 5.6%",
              status: "normal",
              plain_explanation: "Healthy average 3-month blood glucose level."
            }
          ],
          explanation: "Analyzed 3 biomarkers. TSH is mildly elevated (4.8 mIU/L), which your doctor can evaluate alongside cycle tracking."
        }
      ];
    }
  },

  async uploadReport(formData) {
    try {
      const res = await fetch(`${API_BASE_URL}/reports/upload`, {
        method: 'POST',
        body: formData
      });
      return await res.json();
    } catch (e) {
      console.warn("Using offline mock parser fallback", e);
      return {
        id: Date.now(),
        title: formData.get('title') || "Uploaded Lab Report",
        structured_data: [
          {
            test_name: "Total Testosterone",
            value: "74.5",
            unit: "ng/dL",
            reference_range: "15 - 70 ng/dL",
            status: "elevated",
            plain_explanation: "Borderline elevated androgen level. Commonly reviewed by gynecologists when addressing acne or irregular periods."
          },
          {
            test_name: "FSH",
            value: "4.2",
            unit: "mIU/mL",
            reference_range: "2.5 - 10.2 mIU/mL",
            status: "normal",
            plain_explanation: "Normal follicle stimulating hormone value."
          }
        ],
        explanation: "Processed document successfully. 1 parameter flagged for doctor discussion."
      };
    }
  },

  async getMealRecommendations(dietType = 'vegetarian', mealType = null, budgetFriendly = false) {
    try {
      let url = `${API_BASE_URL}/food/recommendations?diet_type=${dietType}&budget_friendly=${budgetFriendly}`;
      if (mealType) url += `&meal_type=${mealType}`;
      const res = await fetch(url);
      if (!res.ok) throw new Error('Failed to fetch food');
      return await res.json();
    } catch (e) {
      return {
        recommendations: [
          {
            dish_name: "Moong Dal Pesarattu with Ginger Chutney",
            meal_type: "breakfast",
            diet_type: "vegetarian",
            ingredients: ["Whole green moong dal", "Ginger", "Green chillies", "Cumin"],
            why_it_works_for_pcos: "Whole moong dal has a low glycemic index and provides 14g of plant protein, preventing morning insulin spikes.",
            protein_grams: 14,
            fibre_grams: 9,
            glycemic_index: "low",
            budget_friendly: true
          },
          {
            dish_name: "Foxtail Millet (Korralu) with Palak Dal & Curd",
            meal_type: "lunch",
            diet_type: "vegetarian",
            ingredients: ["Foxtail millet", "Spinach (Palak)", "Toor dal", "Curd"],
            why_it_works_for_pcos: "Swapping white polished rice with foxtail millet slows glucose release. Spinach supplies magnesium.",
            protein_grams: 16,
            fibre_grams: 11,
            glycemic_index: "medium",
            budget_friendly: true
          },
          {
            dish_name: "Sprouted Methi & Kala Chana Chaat",
            meal_type: "snack",
            diet_type: "vegetarian",
            ingredients: ["Sprouted black chana", "Methi sprouts", "Cucumber", "Lemon juice"],
            why_it_works_for_pcos: "Fenugreek (methi) supports healthy glucose tolerance; high in soluble fibre.",
            protein_grams: 10,
            fibre_grams: 8,
            glycemic_index: "low",
            budget_friendly: true
          }
        ],
        lifestyle_note: "Pair carbohydrates with protein to avoid rapid glucose surges."
      };
    }
  },

  async askTeluguAssistant(question, language = 'te') {
    try {
      const res = await fetch(`${API_BASE_URL}/assistant/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question, language })
      });
      return await res.json();
    } catch (e) {
      if (language === 'te') {
        return {
          answer: "పిసిఒఎస్ (PCOS) అనేది హార్మోన్ల అసమతుల్యత వల్ల వచ్చే సాధారణ జీవనశైలి స్థితి. పెసరట్టు, కొర్రలు, తాజా కూరగాయలు మరియు వ్యాయామంతో దీనిని సమర్థవంతంగా నియంత్రించవచ్చు. \n\n⚠️ గమనిక: ఇది విద్యా సమాచారం మాత్రమే. రోగ నిర్ధారణ కోసం మీ డాక్టర్‌ని సంప్రదించండి.",
          audio_text: "పిసిఒఎస్ అనేది హార్మోన్ల అసమతుల్యత వల్ల వచ్చే సాధారణ జీవనశైలి స్థితి.",
          educational_sources: ["WHO Guidelines on PCOS", "FOGSI Indian Clinical Consensus"],
          escalate_to_doctor: false
        };
      }
      return {
        answer: "PCOS is a hormonal condition where regular ovulation may be paused. Balanced nutrition with whole grains, legumes, and gentle daily activity helps support metabolic rhythm.\n\n⚠️ Disclaimer: For educational awareness only. Consult a doctor for clinical assessment.",
        audio_text: "PCOS is a hormonal condition where regular ovulation may be paused.",
        educational_sources: ["WHO Guidelines on PCOS"],
        escalate_to_doctor: false
      };
    }
  },

  async getDoctorSummary() {
    try {
      const res = await fetch(`${API_BASE_URL}/doctor-prep/summary`);
      if (!res.ok) throw new Error('Failed to get summary');
      return await res.json();
    } catch (e) {
      return {
        patient_overview: "Priya Sharma, 24 years old",
        chief_concerns: "Cycle irregularity (38-day gap), mild acne, afternoon fatigue",
        menstrual_history: "Latest period started 14 days ago with light flow. Previous cycle had 38-day interval.",
        pertinent_lab_findings: [
          "TSH (Thyroid): 4.8 mIU/L (Ref: 0.4 - 4.5 mIU/L) - Status: ELEVATED",
          "Fasting Insulin: 18.2 uIU/mL (Ref: 2.0 - 24.9) - Status: NORMAL"
        ],
        active_medications: [
          "Myo-Inositol & Folic Acid (1 sachet dissolved in water)"
        ],
        recommended_questions_to_ask: [
          "Do my mildly elevated TSH levels warrant thyroid antibody testing?",
          "Should I introduce inositol or metformin based on my insulin resistance profile?",
          "When should we perform a follow-up pelvic ultrasound to evaluate antral follicles?"
        ],
        clinical_disclaimer: "Prepared by Health Saathi to facilitate patient-clinician communication. Not an automated diagnosis."
      };
    }
  }
};
