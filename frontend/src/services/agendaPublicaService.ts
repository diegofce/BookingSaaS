import axiosClient from '../api/axiosClient';
import { endpoints } from '../api/endpoints';
import type { ReservaPayload, ServicioPublico } from '../types/public';

interface BackendReservaPayload {
  servicio_id: number;
  fecha_inicio: string;
  cliente_nombre: string;
  cliente_email?: string;
  cliente_telefono?: string;
}

export const agendaPublicaService = {
  async servicios(dominio: string): Promise<ServicioPublico[]> {
    const { data } = await axiosClient.get<ServicioPublico[]>(`${endpoints.agendaPublica}/${dominio}/servicios`);
    return data;
  },
  async disponibilidad(dominio: string, servicioId: number, fecha: string): Promise<string[]> {
    const { data } = await axiosClient.get<string[]>(`${endpoints.agendaPublica}/${dominio}/disponibilidad`, {
      params: { servicio_id: servicioId, fecha },
    });
    return data;
  },
  async reservar(dominio: string, payload: ReservaPayload): Promise<{ cita: { id: number } }> {
    // Backend contract currently accepts fecha_inicio + cliente_nombre + cliente_telefono.
    const backendPayload: BackendReservaPayload = {
      servicio_id: payload.servicio_id,
      fecha_inicio: new Date(`${payload.fecha}T${payload.hora}:00`).toISOString(),
      cliente_nombre: payload.nombre,
      cliente_email: payload.email,
      cliente_telefono: payload.telefono,
    };

    const { data } = await axiosClient.post<{ cita: { id: number } }>(`${endpoints.agendaPublica}/${dominio}/reservar`, backendPayload);
    return data;
  },
};
