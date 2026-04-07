export const sanitizeText = (value: string): string =>
  value.replace(/[<>]/g, '').trim();

export const required = (value: string, label: string): string | null => {
  if (!value.trim()) return `${label} es requerido`;
  return null;
};

export const validateEmail = (value: string): string | null => {
  if (!value) return 'Email es requerido';
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(value) ? null : 'Email no válido';
};
