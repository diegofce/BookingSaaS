export const formatDateTime = (value: string): string =>
  new Date(value).toLocaleString();

export const toISODate = (value: Date): string => value.toISOString().split('T')[0];
