export const extractTenant = (hostname: string = window.location.hostname): string => {
  const hostParts = hostname.split('.');
  if (hostParts.length < 3) {
    return 'default';
  }
  return hostParts[0] || 'default';
};
