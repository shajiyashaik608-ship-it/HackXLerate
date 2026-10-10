import React from 'react';

export default function FormField({
  label,
  id,
  type = 'text',
  value,
  onChange,
  error = '',
  hint = '',
  required = false,
  placeholder = '',
  children = null, // for select or custom inputs
  ...rest
}) {
  return (
    <div className="form-group" style={{ marginBottom: '16px' }}>
      {label && (
        <label
          htmlFor={id}
          className="form-label"
          style={{
            display: 'block',
            fontSize: '0.84rem',
            fontWeight: 600,
            color: 'var(--text-primary)',
            marginBottom: '6px'
          }}
        >
          {label} {required && <span style={{ color: 'var(--coral-500)' }}>*</span>}
        </label>
      )}

      {children ? (
        children
      ) : (
        <input
          id={id}
          type={type}
          value={value}
          onChange={onChange}
          placeholder={placeholder}
          aria-invalid={Boolean(error)}
          aria-describedby={error ? `${id}-error` : hint ? `${id}-hint` : undefined}
          style={{
            width: '100%',
            borderColor: error ? 'var(--coral-500)' : 'var(--border-subtle)'
          }}
          {...rest}
        />
      )}

      {hint && !error && (
        <span
          id={`${id}-hint`}
          className="form-hint"
          style={{ display: 'block', fontSize: '0.76rem', color: 'var(--text-muted)', marginTop: '4px' }}
        >
          {hint}
        </span>
      )}

      {error && (
        <span
          id={`${id}-error`}
          role="alert"
          style={{ display: 'block', fontSize: '0.78rem', color: 'var(--coral-600)', marginTop: '4px', fontWeight: 500 }}
        >
          {error}
        </span>
      )}
    </div>
  );
}
