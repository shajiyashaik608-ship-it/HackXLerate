import { useState, useEffect, useCallback } from 'react';

/**
 * Custom hook for Web Speech Synthesis (Text-to-Speech)
 * Automatically discovers available regional voices for te-IN and en-IN.
 */
export function useSpeechSynthesis() {
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [isSupported, setIsSupported] = useState(true);

  useEffect(() => {
    if (!('speechSynthesis' in window)) {
      setIsSupported(false);
    }
  }, []);

  const speak = useCallback((text, language = 'en') => {
    if (!('speechSynthesis' in window)) return;

    window.speechSynthesis.cancel();
    if (!text || !text.trim()) return;

    // Clean markdown and symbols from speech text
    const cleanText = text
      .replace(/[#*`_~]/g, '')
      .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1')
      .trim();

    const utterance = new SpeechSynthesisUtterance(cleanText);
    utterance.lang = language === 'te' ? 'te-IN' : 'en-IN';
    utterance.rate = 0.95;

    // Look for matching regional voice if available
    const voices = window.speechSynthesis.getVoices();
    const targetLang = language === 'te' ? 'te' : 'en';
    const match = voices.find((v) => v.lang.toLowerCase().startsWith(targetLang));
    if (match) {
      utterance.voice = match;
    }

    utterance.onstart = () => setIsSpeaking(true);
    utterance.onend = () => {
      setIsSpeaking(false);
      if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
      }
    };
    utterance.onerror = () => {
      setIsSpeaking(false);
      if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
      }
    };

    window.speechSynthesis.speak(utterance);
  }, []);

  const stop = useCallback(() => {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      setIsSpeaking(false);
    }
  }, []);

  return {
    speak,
    stop,
    isSpeaking,
    isSupported
  };
}
