import type { ButtonHTMLAttributes } from 'react';

interface Props extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger';
}

export const Button = ({ variant = 'primary', className = '', ...props }: Props) => {
  const variants = {
    primary: 'bg-brand-500 text-white hover:bg-brand-700',
    secondary: 'bg-slate-200 text-slate-900 hover:bg-slate-300',
    danger: 'bg-red-600 text-white hover:bg-red-700',
  };

  return (
    <button
      className={`rounded-md px-3 py-2 text-sm font-medium transition disabled:opacity-60 ${variants[variant]} ${className}`}
      {...props}
    />
  );
};
