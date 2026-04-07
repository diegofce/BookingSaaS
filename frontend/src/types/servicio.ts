export interface Servicio {
  id: number;
  nombre: string;
  descripcion?: string | null;
  duracion_minutos: number;
  precio: string;
  activo: boolean;
}

export interface ServicioPayload {
  nombre: string;
  descripcion?: string;
  duracion_minutos: number;
  precio: string;
  activo: boolean;
}
