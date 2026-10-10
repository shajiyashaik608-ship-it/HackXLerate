import React from 'react';

export default function Button({
  children,
  variant = 'primary', // primary, secondary, coral, outline, ghost
  size = 'md',        // sm, md, lg
  onClick,
  disabled = false,
  type = 'button',
  icon = null,
  className = '',
  title = ''
}) {
  const variantClass = `btn-${variant}`;
  const sizeClass = size !== 'md' ? `btn-${size}` : '';

  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className={`btn ${variantClass} ${sizeClass} ${className}`}
      title={title}
    >
      {icon && <span className="btn-icon">{icon}</span>}
      <span>{children}</span>
    </button>
  );
}
