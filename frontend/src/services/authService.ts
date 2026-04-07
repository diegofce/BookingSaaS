import axiosClient from '../api/axiosClient';
import { endpoints } from '../api/endpoints';
import type { AuthUser, LoginRequest, TokenResponse } from '../types/auth';

export const authService = {
  async login(payload: LoginRequest): Promise<TokenResponse> {
    const { data } = await axiosClient.post<TokenResponse>(endpoints.auth.login, payload);
    return data;
  },
  async refresh(): Promise<TokenResponse> {
    const { data } = await axiosClient.post<TokenResponse>('/auth/refresh');
    return data;
  },
  async logout(): Promise<void> {
    await axiosClient.post('/auth/logout');
  },
  async me(): Promise<AuthUser> {
    const { data } = await axiosClient.get<AuthUser>(endpoints.auth.me);
    return data;
  },
};
