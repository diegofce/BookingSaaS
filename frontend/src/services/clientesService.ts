import axiosClient from '../api/axiosClient';
import { endpoints } from '../api/endpoints';
import type { Cliente, ClientePayload } from '../types/cliente';

export const clientesService = {
  async getAll(): Promise<Cliente[]> {
    const { data } = await axiosClient.get<Cliente[]>(endpoints.clientes);
    return data;
  },
  async create(payload: ClientePayload): Promise<Cliente> {
    const { data } = await axiosClient.post<Cliente>(endpoints.clientes, payload);
    return data;
  },
  async update(id: number, payload: Partial<ClientePayload>): Promise<Cliente> {
    const { data } = await axiosClient.put<Cliente>(`${endpoints.clientes}/${id}`, payload);
    return data;
  },
  async remove(id: number): Promise<void> {
    await axiosClient.delete(`${endpoints.clientes}/${id}`);
  },
};
