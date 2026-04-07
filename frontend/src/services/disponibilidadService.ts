import axiosClient from '../api/axiosClient';

export const disponibilidadService = {
  async getByServicio(servicioId: number, fecha: string): Promise<string[]> {
    const { data } = await axiosClient.get<string[]>('/citas/disponibilidad', {
      params: { servicio_id: servicioId, fecha },
    });
    return data;
  },
};
