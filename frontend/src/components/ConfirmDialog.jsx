import React from 'react';
import Modal from './Modal';

export default function ConfirmDialog({
  isOpen,
  title = 'Confirm Action',
  message,
  confirmLabel = 'Confirm',
  cancelLabel = 'Cancel',
  isDestructive = false,
  onConfirm,
  onCancel
}) {
  if (!isOpen) return null;

  return (
    <Modal
      isOpen={isOpen}
      onClose={onCancel}
      title={title}
      maxWidth="460px"
      footer={
        <div style={{ display: 'flex', gap: '10px', justifyContent: 'flex-end', width: '100%' }}>
          <button onClick={onCancel} className="btn btn-outline btn-sm">
            {cancelLabel}
          </button>
          <button
            onClick={onConfirm}
            className={`btn btn-sm ${isDestructive ? 'btn-coral' : 'btn-primary'}`}
          >
            {confirmLabel}
          </button>
        </div>
      }
    >
      <div style={{ padding: '8px 0', fontSize: '0.9rem', color: 'var(--text-secondary)', lineHeight: 1.6 }}>
        {message}
      </div>
    </Modal>
  );
}
