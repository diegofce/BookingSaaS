import { useMemo } from 'react';
import { extractTenant } from '../utils/tenant';

export const useTenant = () => {
  const tenant = useMemo(() => extractTenant(), []);
  return { tenant };
};
