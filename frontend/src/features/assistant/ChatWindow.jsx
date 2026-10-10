import React, { useState, useRef, useEffect } from 'react';
import ChatMessage from '../../components/ChatMessage';
import QuickQuestions from './QuickQuestions';
import LanguageSelector from './LanguageSelector';
import ConfirmDialog from '../../components/ConfirmDialog';
import { healthAssistantService } from '../../services/healthAssistantService';
import { useSpeechRecognition } from '../../hooks/useSpeechRecognition';
import { useSpeechSynthesis } from '../../hooks/useSpeechSynthesis';

export default function ChatWindow({ language, setLanguage, chatHistory, setChatHistory }) {
  const [inputText, setInputText] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [showClearConfirm, setShowClearConfirm] = useState(false);
  const [voiceError, setVoiceError] = useState('');
  const messagesEndRef = useRef(null);

  const { speak, stop: stopSpeech, isSpeaking } = useSpeechSynthesis();

  const handleSpeechResult = (transcript) => {
    setInputText(transcript);
    handleSend(transcript);
  };

  const handleSpeechError = (msg) => {
    setVoiceError(msg);
    setTimeout(() => setVoiceError(''), 4000);
  };

  const { isListening, isSupported: sttSupported, startListening, stopListening } = useSpeechRecognition({
    language,
    onResult: handleSpeechResult,
    onError: handleSpeechError
  });

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [chatHistory, isTyping]);

  const handleSend = async (textToSend = null) => {
    const text = textToSend || inputText;
    if (!text || !text.trim()) return;

    const userMessage = {
      id: Date.now(),
      sender: 'user',
      text: text.trim(),
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setChatHistory((prev) => [...prev, userMessage]);
    setInputText('');
    setIsTyping(true);

    try {
      const response = await healthAssistantService.queryAssistant(text, language);
      const assistantMessage = {
        id: Date.now() + 1,
        sender: 'assistant',
        text: response.answer,
        sources: response.sources,
        disclaimer: response.disclaimer,
        isUrgent: response.isUrgent,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      setChatHistory((prev) => [...prev, assistantMessage]);
    } catch (err) {
      console.error(err);
    } finally {
      setIsTyping(false);
    }
  };

  const confirmClearChat = () => {
    setChatHistory([
      {
        id: 1,
        sender: 'assistant',
        text: language === 'te'
          ? "నమస్తే! నేను మీ పిసిఒఎస్ సాథి AI అసిస్టెంట్. పీరియడ్స్, ఆహారపు అలవాట్లు లేదా రిపోర్టుల గురించి ఏదైనా అడగండి."
          : "Hello! I am your PCOS Saathi companion. Ask me any health-education questions about cycle rhythms, Indian meals, or doctor visit preparation.",
        sources: ["WHO Guidelines", "FOGSI"],
        disclaimer: "Educational simulation only. Consult a doctor for medical diagnoses.",
        timestamp: 'Just now'
      }
    ]);
    setShowClearConfirm(false);
  };

  const handlePlayAudio = (text) => {
    if (isSpeaking) {
      stopSpeech();
    } else {
      speak(text, language);
    }
  };

  const toggleMic = () => {
    if (isListening) {
      stopListening();
    } else {
      startListening();
    }
  };

  return (
    <div className="card" style={{ padding: 0, overflow: 'hidden', display: 'flex', flexDirection: 'column', height: '650px' }}>
      {/* Chat Header */}
      <div style={{
        padding: '14px 20px',
        borderBottom: '1px solid var(--border-subtle)',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        background: 'var(--bg-subtle)'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <div style={{
            width: '36px',
            height: '36px',
            borderRadius: '50%',
            background: 'var(--primary-100)',
            color: 'var(--primary-800)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: '1.2rem'
          }}>
            🌿
          </div>
          <div>
            <div style={{ fontWeight: 700, fontSize: '0.94rem', color: 'var(--text-primary)' }}>
              PCOS Saathi AI Copilot
            </div>
            <div style={{ fontSize: '0.74rem', color: 'var(--primary-700)', display: 'flex', alignItems: 'center', gap: '6px' }}>
              <span style={{ width: '8px', height: '8px', borderRadius: '50%', background: '#22c55e', display: 'inline-block' }} />
              {isListening ? '🎤 Listening in Telugu/English...' : isSpeaking ? '🔊 Speaking...' : 'Ready (Bilingual Voice Enabled)'}
            </div>
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <LanguageSelector currentLanguage={language} onSelectLanguage={setLanguage} />
          <button
            onClick={() => setShowClearConfirm(true)}
            className="btn btn-ghost btn-sm"
            title="Clear Chat History"
            style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}
          >
            Clear
          </button>
        </div>
      </div>

      {voiceError && (
        <div style={{
          background: 'var(--coral-50)',
          color: 'var(--coral-700)',
          padding: '6px 14px',
          fontSize: '0.78rem',
          borderBottom: '1px solid var(--coral-500)',
          display: 'flex',
          justifyContent: 'space-between'
        }}>
          <span>⚠️ {voiceError}</span>
          <button onClick={() => setVoiceError('')} style={{ color: 'var(--coral-700)' }}>✕</button>
        </div>
      )}

      {/* Messages Scroll View */}
      <div style={{
        flex: 1,
        padding: '20px',
        overflowY: 'auto',
        display: 'flex',
        flexDirection: 'column',
        gap: '16px',
        backgroundColor: '#ffffff'
      }}>
        {chatHistory.map((msg) => (
          <ChatMessage
            key={msg.id}
            message={msg}
            onPlayAudio={handlePlayAudio}
            isPlaying={isSpeaking}
          />
        ))}

        {isTyping && (
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--text-muted)', fontSize: '0.82rem', padding: '6px 10px' }}>
            <span className="spinner" style={{ width: '16px', height: '16px', border: '2px solid var(--border-subtle)', borderTopColor: 'var(--primary-700)', borderRadius: '50%', animation: 'spin 0.8s linear infinite' }} />
            <span>Saathi is formulating grounded advice...</span>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Suggested Quick Question Chips */}
      <QuickQuestions language={language} onSelectQuestion={(q) => handleSend(q)} />

      {/* Input Bar */}
      <form
        onSubmit={(e) => { e.preventDefault(); handleSend(); }}
        style={{
          padding: '12px 18px',
          borderTop: '1px solid var(--border-subtle)',
          backgroundColor: 'var(--bg-card)',
          display: 'flex',
          alignItems: 'center',
          gap: '10px'
        }}
      >
        <button
          type="button"
          onClick={toggleMic}
          className={`btn btn-sm ${isListening ? 'btn-coral' : 'btn-outline'}`}
          style={{
            borderRadius: '50%',
            width: '42px',
            height: '42px',
            padding: 0,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: '1.2rem',
            position: 'relative'
          }}
          title={isListening ? "Stop listening" : "Click to speak in Telugu or English"}
        >
          {isListening ? '⏹️' : '🎙️'}
        </button>

        <input
          type="text"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          placeholder={
            language === 'te'
              ? 'పీరియడ్స్, ఆహారపు అలవాట్లు లేదా రిపోర్టుల గురించి అడగండి...'
              : 'Ask about menstrual cycles, Indian meals, or lab terminology...'
          }
          style={{
            flex: 1,
            borderRadius: 'var(--radius-full)',
            padding: '10px 18px',
            fontSize: '0.88rem'
          }}
        />

        <button
          type="submit"
          disabled={!inputText.trim() || isTyping}
          className="btn btn-primary"
          style={{
            borderRadius: 'var(--radius-full)',
            padding: '10px 20px',
            fontSize: '0.86rem'
          }}
        >
          <span>Send</span>
          <span>→</span>
        </button>
      </form>

      {/* Confirm Clear Chat Dialog */}
      <ConfirmDialog
        isOpen={showClearConfirm}
        title="Clear Conversation History"
        message="Are you sure you want to reset the conversation history? This cannot be undone."
        confirmLabel="Clear Conversation"
        isDestructive={true}
        onConfirm={confirmClearChat}
        onCancel={() => setShowClearConfirm(false)}
      />
    </div>
  );
}
