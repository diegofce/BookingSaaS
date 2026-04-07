import { useState } from 'react';
import { DashboardLayout } from '../components/layout/DashboardLayout';
import { useAuth } from '../auth/useAuth';
import { useFetch } from '../hooks/useFetch';
import { empleadosService } from '../services/empleadosService';
import { Card } from '../components/ui/Card';
import { Input } from '../components/ui/Input';
import { Button } from '../components/ui/Button';
import { useToast } from '../state/useToast';
import type { Empleado } from '../types/empleado';

export const EmpleadosPage = () => {
  const { user } = useAuth();
  const { data, setData } = useFetch(empleadosService.getAll, []);
  const { success, error } = useToast();
  const [nombre, setNombre] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [editingId, setEditingId] = useState<number | null>(null);
  const [editing, setEditing] = useState<{ nombre: string; email: string; activo: boolean }>({
    nombre: '',
    email: '',
    activo: true,
  });

  if (user?.rol !== 'admin') {
    return <DashboardLayout><Card>Solo admin puede gestionar empleados.</Card></DashboardLayout>;
  }

  const refresh = async () => setData(await empleadosService.getAll());
  const startEdit = (empleado: Empleado) => {
    setEditingId(empleado.id);
    setEditing({
      nombre: empleado.nombre,
      email: empleado.email,
      activo: empleado.activo,
    });
  };

  return (
    <DashboardLayout>
      <Card>
        <h2 className="mb-3 font-semibold">Nuevo empleado</h2>
        <div className="grid gap-2 md:grid-cols-4">
          <Input label="Nombre" value={nombre} onChange={(e) => setNombre(e.target.value)} />
          <Input label="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
          <Input label="Password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
          <Button
            className="self-end"
            onClick={async () => {
              try {
                await empleadosService.create({ nombre, email, password, rol: 'empleado', activo: true });
                setNombre('');
                setEmail('');
                setPassword('');
                await refresh();
                success('Empleado creado');
              } catch {
                error('No se pudo crear el empleado');
              }
            }}
          >
            Crear
          </Button>
        </div>
      </Card>

      <Card>
        <table className="w-full text-sm">
          <thead><tr className="text-left"><th>Nombre</th><th>Email</th><th>Rol</th><th></th></tr></thead>
          <tbody>
            {(data || []).map((e) => (
              <tr key={e.id} className="border-t">
                <td>
                  {editingId === e.id ? (
                    <input
                      className="rounded border px-2 py-1 text-sm"
                      value={editing.nombre}
                      onChange={(ev) => setEditing((prev) => ({ ...prev, nombre: ev.target.value }))}
                    />
                  ) : e.nombre}
                </td>
                <td>
                  {editingId === e.id ? (
                    <input
                      className="rounded border px-2 py-1 text-sm"
                      value={editing.email}
                      onChange={(ev) => setEditing((prev) => ({ ...prev, email: ev.target.value }))}
                    />
                  ) : e.email}
                </td>
                <td>{e.rol}</td>
                <td className="text-right">
                  <div className="flex justify-end gap-2">
                    {editingId === e.id ? (
                      <Button
                        variant="secondary"
                        onClick={async () => {
                          try {
                            await empleadosService.update(e.id, {
                              nombre: editing.nombre,
                              email: editing.email,
                              activo: editing.activo,
                            });
                            setEditingId(null);
                            await refresh();
                            success('Empleado actualizado');
                          } catch {
                            error('No se pudo actualizar el empleado');
                          }
                        }}
                      >
                        Guardar
                      </Button>
                    ) : (
                      <Button variant="secondary" onClick={() => startEdit(e)}>Editar</Button>
                    )}
                    <Button
                      variant="danger"
                      onClick={async () => {
                        try {
                          await empleadosService.remove(e.id);
                          await refresh();
                          success('Empleado eliminado');
                        } catch {
                          error('No se pudo eliminar el empleado');
                        }
                      }}
                    >
                      Eliminar
                    </Button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </Card>
    </DashboardLayout>
  );
};
