export interface Empleado {
  id: number;
  nombre: string;
  email: string;
  rol: 'admin' | 'empleado' | 'cliente';
  activo: boolean;
}

export interface EmpleadoPayload {
  nombre: string;
  email: string;
  password?: string;
  rol: 'admin' | 'empleado';
  activo: boolean;
}
