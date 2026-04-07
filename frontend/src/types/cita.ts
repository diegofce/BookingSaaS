export interface Cita {
  id: number;
  cliente_id: number;
  servicio_id: number;
  empleado_id?: number | null;
  fecha_inicio: string;
  fecha_fin: string;
  estado: 'pendiente' | 'confirmada' | 'cancelada';
  monto_pagado: string;
}

export interface CitaPayload {
  cliente_id: number;
  servicio_id: number;
  empleado_id?: number;
  fecha_inicio: string;
  monto_pagado: string;
}
