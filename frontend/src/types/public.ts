export interface ServicioPublico {
  id: number;
  nombre: string;
  descripcion?: string | null;
  duracion_minutos: number;
  precio: string;
  activo: boolean;
}

export interface DisponibilidadSlot {
  hora: string;
  disponible: boolean;
}

export interface ReservaPayload {
  servicio_id: number;
  fecha: string;
  hora: string;
  nombre: string;
  email: string;
  telefono: string;
}
