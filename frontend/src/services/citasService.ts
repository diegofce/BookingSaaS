import axiosClient from '../api/axiosClient';
import { endpoints } from '../api/endpoints';
import type { Cita, CitaPayload } from '../types/cita';

export const citasService = {
  async getAll(): Promise<Cita[]> {
    const { data } = await axiosClient.get<Cita[]>(endpoints.citas);
    return data;
  },
  async create(payload: CitaPayload): Promise<Cita> {
    const { data } = await axiosClient.post<Cita>(endpoints.citas, payload);
    return data;
  },
  async update(id: number, payload: Partial<CitaPayload>): Promise<Cita> {
    const { data } = await axiosClient.put<Cita>(`${endpoints.citas}/${id}`, payload);
    return data;
  },
  async remove(id: number): Promise<void> {
    await axiosClient.delete(`${endpoints.citas}/${id}`);
  },
};
