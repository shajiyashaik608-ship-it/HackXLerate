import { useState, useEffect, useRef, useCallback } from 'react';

/**
 * Custom hook for W3C Web Speech SpeechRecognition
 * Supports te-IN (Telugu) and en-IN (English) with robust error & permission handling.
 */
export function useSpeechRecognition({ language = 'en', onResult, onError }) {
  const [isListening, setIsListening] = useState(false);
  const [isSupported, setIsSupported] = useState(true);
  const [errorMessage, setErrorMessage] = useState('');
  const recognitionRef = useRef(null);

  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      setIsSupported(false);
      return;
    }

    try {
      const recognition = new SpeechRecognition();
      recognition.continuous = false;
      recognition.interimResults = false;
      recognition.lang = language === 'te' ? 'te-IN' : 'en-IN';

      recognition.onstart = () => {
        setIsListening(true);
        setErrorMessage('');
      };

      recognition.onend = () => {
        setIsListening(false);
      };

      recognition.onerror = (event) => {
        setIsListening(false);
        let msg = 'Voice recognition encountered an issue.';
        if (event.error === 'not-allowed') {
          msg = 'Microphone permission was denied. Please allow microphone access in browser settings.';
        } else if (event.error === 'no-speech') {
          msg = 'No speech was detected. Please try speaking again.';
        } else if (event.error === 'network') {
          msg = 'Network connection needed for browser speech recognition.';
        }
        setErrorMessage(msg);
        if (onError) onError(msg);
      };

      recognition.onresult = (event) => {
        if (event.results && event.results[0] && event.results[0][0]) {
          const transcript = event.results[0][0].transcript;
          if (onResult) onResult(transcript);
        }
      };

      recognitionRef.current = recognition;
    } catch (err) {
      setIsSupported(false);
      setErrorMessage('Speech recognition initialization failed.');
    }

    return () => {
      if (recognitionRef.current) {
        recognitionRef.current.abort();
      }
    };
  }, [language, onResult, onError]);

  const startListening = useCallback(() => {
    setErrorMessage('');
    if (!recognitionRef.current) {
      setErrorMessage('Speech recognition is not available in this browser.');
      return;
    }
    try {
      recognitionRef.current.lang = language === 'te' ? 'te-IN' : 'en-IN';
      recognitionRef.current.start();
    } catch (e) {
      console.warn('Recognition start error:', e);
    }
  }, [language]);

  const stopListening = useCallback(() => {
    if (recognitionRef.current) {
      recognitionRef.current.stop();
    }
  }, []);

  return {
    isListening,
    isSupported,
    errorMessage,
    startListening,
    stopListening
  };
}
