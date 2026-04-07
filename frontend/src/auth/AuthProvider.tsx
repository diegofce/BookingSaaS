import { useCallback, useEffect, useMemo, useState } from 'react';
import type { ReactNode } from 'react';
import { AuthContext } from './AuthContext';
import type { LoginRequest, AuthUser } from '../types/auth';
import { authService } from '../services/authService';
import { setAuthToken, setUnauthorizedHandler } from '../api/axiosClient';

interface Props {
  children: ReactNode;
}

export const AuthProvider = ({ children }: Props) => {
  const [token, setToken] = useState<string | null>(null);
  const [user, setUser] = useState<AuthUser | null>(null);
  const [loading, setLoading] = useState(false);

  const logout = useCallback(() => {
    authService.logout().catch(() => undefined);
    setToken(null);
    setUser(null);
    setAuthToken(null);
  }, []);

  const login = useCallback(async (payload: LoginRequest) => {
    setLoading(true);
    try {
      const session = await authService.login(payload);
      setToken(session.access_token);
      setAuthToken(session.access_token);
      const me = await authService.me();
      setUser(me);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    setUnauthorizedHandler(logout);
    return () => setUnauthorizedHandler(null);
  }, [logout]);

  useEffect(() => {
    let mounted = true;
    setLoading(true);
    authService
      .refresh()
      .then(async (session) => {
        if (!mounted) return;
        setToken(session.access_token);
        setAuthToken(session.access_token);
        const me = await authService.me();
        if (!mounted) return;
        setUser(me);
      })
      .catch(() => {
        if (!mounted) return;
        setToken(null);
        setUser(null);
        setAuthToken(null);
      })
      .finally(() => {
        if (mounted) setLoading(false);
      });
    return () => {
      mounted = false;
    };
  }, []);

  const value = useMemo(
    () => ({ token, user, loading, login, logout, isAuthenticated: Boolean(token && user) }),
    [token, user, loading, login, logout]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
