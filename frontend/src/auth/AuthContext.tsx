import { createContext } from 'react';
import type { AuthUser, LoginRequest } from '../types/auth';

export interface AuthContextValue {
  token: string | null;
  user: AuthUser | null;
  loading: boolean;
  login: (payload: LoginRequest) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
}

export const AuthContext = createContext<AuthContextValue | undefined>(undefined);
