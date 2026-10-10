import React, { useState } from 'react';
import { apiClient } from '../api/client';

export default function TeluguVoiceAssistant({ language, setLanguage }) {
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState([
    {
      sender: 'saathi',
      text: language === 'te' 
        ? "నమస్తే! నేను మీ పిసిఒఎస్ సాథిని. మీకు పీరియడ్స్, ఆహారం, లేదా రిపోర్టుల గురించి ఎలాంటి ప్రశ్నలున్నా అడగండి."
        : "Hello! I am your PCOS Saathi. Ask me any questions about cycles, nutrition, or your lab reports.",
      audioText: "నమస్తే! నేను మీ పిసిఒఎస్ సాథిని.",
      sources: ["FOGSI Guidelines", "ICMR Nutrition"]
    }
  ]);
  const [isListening, setIsListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const teluguQuickChips = [
    "PCOS అంటే ఏమిటి? సులభంగా వివరించండి.",
    "పీరియడ్స్ సరిగ్గా రాకపోతే ఎప్పుడు డాక్టర్‌ని కలవాలి?",
    "PCOS ఉన్నప్పుడు బరువు తగ్గడానికి ఎలాంటి ఆహారం తీసుకోవాలి?",
    "హార్మోన్ల అసమతుల్యత ఎలా తెలుస్తుంది?"
  ];

  const englishQuickChips = [
    "What is PCOS? Explain simply.",
    "When should I see a doctor for missed periods?",
    "What South Indian foods help manage insulin resistance?",
    "How does thyroid affect menstrual cycles?"
  ];

  const chips = language === 'te' ? teluguQuickChips : englishQuickChips;

  // Speech Recognition (Web Speech API)
  const handleVoiceInput = () => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      alert("Speech recognition is not supported in this browser. Please type your question.");
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = language === 'te' ? 'te-IN' : 'en-IN';
    recognition.interimResults = false;

    recognition.onstart = () => setIsListening(true);
    recognition.onend = () => setIsListening(false);
    recognition.onerror = () => setIsListening(false);

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      setQuery(transcript);
      handleSend(transcript);
    };

    recognition.start();
  };

  // Text-to-Speech (Web Speech API)
  const playAudio = (text) => {
    if (!('speechSynthesis' in window)) return;
    if (isSpeaking) {
      window.speechSynthesis.cancel();
      setIsSpeaking(false);
      return;
    }
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = language === 'te' ? 'te-IN' : 'en-IN';
    utterance.rate = 0.95;
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
  };

  const handleSend = async (questionText) => {
    const textToSend = questionText || query;
    if (!textToSend.trim()) return;

    const userMsg = { sender: 'user', text: textToSend };
    setMessages((prev) => [...prev, userMsg]);
    setQuery('');
    setIsLoading(true);

    const res = await apiClient.askTeluguAssistant(textToSend, language);
    setIsLoading(false);

    const botMsg = {
      sender: 'saathi',
      text: res.answer,
      audioText: res.audio_text,
      sources: res.educational_sources || [],
      escalate: res.escalate_to_doctor
    };
    setMessages((prev) => [...prev, botMsg]);

    // Auto-play speech if voice was used
    if (res.audio_text && isListening) {
      playAudio(res.audio_text);
    }
  };

  return (
    <div style={{ maxWidth: '900px', margin: '0 auto', padding: '24px 20px' }}>
      <div style={{ textAlign: 'center', marginBottom: '24px' }}>
        <h1 style={{ fontSize: '1.8rem', color: '#0f172a', marginBottom: '6px' }}>
          🎙️ PCOS Saathi — {language === 'te' ? 'తెలుగు వాయిస్ అసిస్టెంట్' : 'Telugu & English Voice Assistant'}
        </h1>
        <p style={{ color: '#64748b', fontSize: '0.92rem' }}>
          {language === 'te'
            ? 'మీ ఆరోగ్య సమస్యలను మీ సొంత భాషలో మాట్లాడి లేదా టైప్ చేసి తెలుసుకోండి.'
            : 'Ask questions in Telugu or English with voice recognition and spoken audio explanations.'}
        </p>
      </div>

      {/* Language Toggle in Chat */}
      <div style={{ display: 'flex', justifyContent: 'center', gap: '8px', marginBottom: '20px' }}>
        <button
          onClick={() => setLanguage('te')}
          style={{
            padding: '6px 16px',
            borderRadius: '20px',
            fontSize: '0.82rem',
            fontWeight: 600,
            background: language === 'te' ? '#e11d48' : '#f1f5f9',
            color: language === 'te' ? 'white' : '#64748b'
          }}
        >
          తెలుగు (Telugu)
        </button>
        <button
          onClick={() => setLanguage('en')}
          style={{
            padding: '6px 16px',
            borderRadius: '20px',
            fontSize: '0.82rem',
            fontWeight: 600,
            background: language === 'en' ? '#0f766e' : '#f1f5f9',
            color: language === 'en' ? 'white' : '#64748b'
          }}
        >
          English
        </button>
      </div>

      {/* Chat Transcript Panel */}
      <div className="glass-panel" style={{
        minHeight: '380px',
        maxHeight: '520px',
        overflowY: 'auto',
        padding: '20px',
        marginBottom: '20px',
        display: 'flex',
        flexDirection: 'column',
        gap: '14px'
      }}>
        {messages.map((m, idx) => (
          <div
            key={idx}
            style={{
              alignSelf: m.sender === 'user' ? 'flex-end' : 'flex-start',
              maxWidth: '82%',
              background: m.sender === 'user' ? '#0f766e' : '#ffffff',
              color: m.sender === 'user' ? '#ffffff' : '#0f172a',
              padding: '14px 18px',
              borderRadius: '16px',
              border: m.sender === 'user' ? 'none' : '1px solid #e2e8f0',
              boxShadow: '0 2px 8px rgba(0,0,0,0.04)'
            }}
          >
            <div style={{ whiteSpace: 'pre-line', fontSize: '0.92rem', lineHeight: '1.6' }}>
              {m.text}
            </div>

            {m.sender === 'saathi' && (
              <div style={{
                marginTop: '10px',
                borderTop: '1px solid #f1f5f9',
                paddingTop: '8px',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                flexWrap: 'wrap',
                gap: '8px'
              }}>
                <div style={{ display: 'flex', gap: '6px' }}>
                  {m.sources?.map((s, i) => (
                    <span key={i} style={{ fontSize: '0.7rem', color: '#64748b', background: '#f8fafc', padding: '2px 6px', borderRadius: '4px' }}>
                      📚 {s}
                    </span>
                  ))}
                </div>

                <button
                  onClick={() => playAudio(m.audioText || m.text)}
                  style={{
                    background: '#ffe4e6',
                    color: '#e11d48',
                    padding: '4px 10px',
                    borderRadius: '8px',
                    fontSize: '0.78rem',
                    fontWeight: 600,
                    display: 'flex',
                    alignItems: 'center',
                    gap: '4px'
                  }}
                >
                  🔊 {isSpeaking ? 'Playing...' : 'Listen'}
                </button>
              </div>
            )}
          </div>
        ))}
        {isLoading && (
          <div style={{ alignSelf: 'flex-start', color: '#64748b', fontSize: '0.85rem' }}>
            Saathi is reviewing trusted medical guidelines...
          </div>
        )}
      </div>

      {/* Suggested Chips */}
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', marginBottom: '16px' }}>
        {chips.map((chip, idx) => (
          <button
            key={idx}
            onClick={() => handleSend(chip)}
            style={{
              background: '#f8fafc',
              border: '1px solid #cbd5e1',
              padding: '6px 12px',
              borderRadius: '999px',
              fontSize: '0.78rem',
              color: '#334155',
              cursor: 'pointer'
            }}
          >
            💬 {chip}
          </button>
        ))}
      </div>

      {/* Input Controls */}
      <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
        <button
          onClick={handleVoiceInput}
          className={isListening ? 'mic-active' : ''}
          style={{
            width: '50px',
            height: '50px',
            borderRadius: '50%',
            background: isListening ? '#e11d48' : '#0f766e',
            color: 'white',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: '1.3rem',
            flexShrink: 0
          }}
          title="Click to speak in Telugu or English"
        >
          {isListening ? '⏹️' : '🎙️'}
        </button>

        <input
          type="text"
          placeholder={language === 'te' ? 'ఇక్కడ మీ ప్రశ్న టైప్ చేయండి...' : 'Type your health question here...'}
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          style={{
            flex: 1,
            padding: '12px 18px',
            borderRadius: '12px',
            border: '1px solid #cbd5e1',
            fontSize: '0.92rem'
          }}
        />

        <button
          onClick={() => handleSend()}
          className="btn-primary"
          style={{ borderRadius: '12px', padding: '12px 20px' }}
        >
          Send
        </button>
      </div>
    </div>
  );
}
