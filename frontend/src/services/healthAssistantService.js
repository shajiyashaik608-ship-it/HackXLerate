/**
 * Health Assistant service for querying grounded bilingual PCOS responses,
 * flagging emergency red flags, and structuring citations.
 */

import { getMockResponse } from '../utils/mockResponses';

export const RED_FLAG_SYMPTOMS = [
  'severe pelvic pain',
  'sudden heavy bleeding',
  'soaking pads every hour',
  'fainting',
  'dizziness with pain',
  'తీవ్రమైన కడుపు నొప్పి',
  'విపరీతమైన రక్తస్రావం',
  'స్పృహ తప్పడం'
];

export const healthAssistantService = {
  checkRedFlags: (message) => {
    const lower = message.toLowerCase();
    return RED_FLAG_SYMPTOMS.some((term) => lower.includes(term.toLowerCase()));
  },

  queryAssistant: async (questionText, language = 'en') => {
    // Artificial latency for natural typing simulation
    await new Promise((res) => setTimeout(res, 650));

    const isUrgent = healthAssistantService.checkRedFlags(questionText);
    const mock = getMockResponse(questionText, language);

    return {
      answer: mock.answer,
      sources: mock.sources || ['WHO Women’s Health Guidelines', 'FOGSI Indian Consensus'],
      disclaimer: isUrgent
        ? '⚠️ EMERGENCY CLINICAL REFERRAL: Severe pelvic pain or intense bleeding requires immediate emergency medical evaluation at a hospital emergency department.'
        : 'Educational simulation only. Not a medical diagnosis.',
      isUrgent: isUrgent || mock.isUrgent
    };
  }
};
