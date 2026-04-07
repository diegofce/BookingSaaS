export interface AuthUser {
  id: number;
  nombre: string;
  email: string;
  rol: 'admin' | 'empleado' | 'cliente';
  activo: boolean;
  negocio_id: number;
}

export interface LoginRequest {
  email: string;
  password: string;
  negocio_id: number;
}

export interface TokenResponse {
  access_token: string;
  token_type?: string;
  user_id?: number;
  negocio_id?: number;
}
