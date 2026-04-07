export interface Cliente {
  id: number;
  nombre: string;
  email?: string | null;
  telefono?: string | null;
  direccion?: string | null;
  barrio?: string | null;
  created_at?: string;
}

export interface ClientePayload {
  nombre: string;
  email?: string;
  telefono?: string;
  direccion?: string;
  barrio?: string;
}
