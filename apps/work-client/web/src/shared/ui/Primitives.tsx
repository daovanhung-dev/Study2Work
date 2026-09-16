import type { ButtonHTMLAttributes, ReactNode } from "react";

type ButtonVariant = "primary" | "secondary" | "quiet" | "danger";

export function Button({
  variant = "primary",
  type = "button",
  className = "",
  children,
  ...props
}: ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: ButtonVariant;
  children: ReactNode;
}) {
  return (
    <button type={type} className={`ui-button ui-button-${variant} ${className}`.trim()} {...props}>
      {children}
    </button>
  );
}

export function PageHeader({
  eyebrow,
  title,
  action,
}: {
  eyebrow: string;
  title: string;
  action?: ReactNode;
}) {
  return (
    <div className="section-heading">
      <div>
        <span className="eyebrow">{eyebrow}</span>
        <h1>{title}</h1>
      </div>
      {action}
    </div>
  );
}

export function Field({
  label,
  htmlFor,
  hint,
  error,
  children,
}: {
  label: string;
  htmlFor?: string;
  hint?: string;
  error?: string;
  children: ReactNode;
}) {
  const hintId = htmlFor && hint ? `${htmlFor}-hint` : undefined;
  const errorId = htmlFor && error ? `${htmlFor}-error` : undefined;
  return (
    <label className="ui-field" htmlFor={htmlFor}>
      <span>{label}</span>
      {children}
      {hint && <small id={hintId}>{hint}</small>}
      {error && <small className="ui-field-error" id={errorId} role="alert">{error}</small>}
    </label>
  );
}

export function StatusBadge({
  children,
  tone = "info",
}: {
  children: ReactNode;
  tone?: "info" | "success" | "warning" | "danger";
}) {
  return <span className={`status-badge status-${tone}`}>{children}</span>;
}

export function Surface({ children, className = "" }: { children: ReactNode; className?: string }) {
  return <section className={`ui-surface ${className}`.trim()}>{children}</section>;
}
