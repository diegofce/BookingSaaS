import axiosClient from '../api/axiosClient';
import { endpoints } from '../api/endpoints';
import type { Empleado, EmpleadoPayload } from '../types/empleado';

export const empleadosService = {
  async getAll(): Promise<Empleado[]> {
    const { data } = await axiosClient.get<Empleado[]>(endpoints.empleados);
    return data.filter((u) => u.rol !== 'cliente');
  },
  async create(payload: EmpleadoPayload): Promise<Empleado> {
    const { data } = await axiosClient.post<Empleado>(`${endpoints.empleados}/`, payload);
    return data;
  },
  async update(id: number, payload: Partial<EmpleadoPayload>): Promise<Empleado> {
    const { data } = await axiosClient.put<Empleado>(`${endpoints.empleados}/${id}`, payload);
    return data;
  },
  async remove(id: number): Promise<void> {
    await axiosClient.delete(`${endpoints.empleados}/${id}`);
  },
};
