import axiosClient from '../api/axiosClient';
import { endpoints } from '../api/endpoints';
import type { Servicio, ServicioPayload } from '../types/servicio';

export const serviciosService = {
  async getAll(): Promise<Servicio[]> {
    const { data } = await axiosClient.get<Servicio[]>(endpoints.servicios);
    return data;
  },
  async create(payload: ServicioPayload): Promise<Servicio> {
    const { data } = await axiosClient.post<Servicio>(endpoints.servicios, payload);
    return data;
  },
  async update(id: number, payload: Partial<ServicioPayload>): Promise<Servicio> {
    const { data } = await axiosClient.put<Servicio>(`${endpoints.servicios}/${id}`, payload);
    return data;
  },
  async remove(id: number): Promise<void> {
    await axiosClient.delete(`${endpoints.servicios}/${id}`);
  },
};
