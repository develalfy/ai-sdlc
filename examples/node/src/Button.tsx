import React from "react";

export type ButtonVariant = "primary" | "secondary";

export interface ButtonProps {
  label: string;
  variant?: ButtonVariant;
  onClick?: () => void;
}

export function Button({ label, variant = "primary", onClick }: ButtonProps) {
  const className = `btn btn--${variant}`;
  return (
    <button
      type="button"
      className={className}
      onClick={onClick}
      aria-label={label}
    >
      {label}
    </button>
  );
}

export default Button;