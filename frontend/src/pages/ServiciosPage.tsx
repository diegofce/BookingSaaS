import { useState } from 'react';
import { DashboardLayout } from '../components/layout/DashboardLayout';
import { useFetch } from '../hooks/useFetch';
import { serviciosService } from '../services/serviciosService';
import { Card } from '../components/ui/Card';
import { Input } from '../components/ui/Input';
import { Button } from '../components/ui/Button';
import { sanitizeText } from '../utils/validators';
import { useToast } from '../state/useToast';
import type { Servicio } from '../types/servicio';

export const ServiciosPage = () => {
  const { data, setData } = useFetch(serviciosService.getAll, []);
  const { success, error } = useToast();
  const [nombre, setNombre] = useState('');
  const [duracion, setDuracion] = useState('30');
  const [precio, setPrecio] = useState('25000');
  const [editingId, setEditingId] = useState<number | null>(null);
  const [editing, setEditing] = useState<{ nombre: string; duracion: string; precio: string }>({
    nombre: '',
    duracion: '30',
    precio: '25000',
  });

  const refresh = async () => setData(await serviciosService.getAll());
  const startEdit = (servicio: Servicio) => {
    setEditingId(servicio.id);
    setEditing({
      nombre: servicio.nombre,
      duracion: String(servicio.duracion_minutos),
      precio: String(servicio.precio),
    });
  };

  return (
    <DashboardLayout>
      <Card>
        <h2 className="mb-3 font-semibold">Nuevo servicio</h2>
        <div className="grid gap-2 md:grid-cols-4">
          <Input label="Nombre" value={nombre} onChange={(e) => setNombre(e.target.value)} />
          <Input label="Duración (min)" value={duracion} onChange={(e) => setDuracion(e.target.value)} />
          <Input label="Precio" value={precio} onChange={(e) => setPrecio(e.target.value)} />
          <Button
            className="self-end"
            onClick={async () => {
              try {
                await serviciosService.create({
                  nombre: sanitizeText(nombre),
                  descripcion: '',
                  duracion_minutos: Number(duracion),
                  precio,
                  activo: true,
                });
                setNombre('');
                await refresh();
                success('Servicio creado');
              } catch {
                error('No se pudo crear el servicio');
              }
            }}
          >
            Crear
          </Button>
        </div>
      </Card>

      <Card>
        <table className="w-full text-sm">
          <thead>
            <tr className="text-left">
              <th>Nombre</th><th>Duración</th><th>Precio</th><th></th>
            </tr>
          </thead>
          <tbody>
            {(data || []).map((s) => (
              <tr key={s.id} className="border-t">
                <td>
                  {editingId === s.id ? (
                    <input
                      className="rounded border px-2 py-1 text-sm"
                      value={editing.nombre}
                      onChange={(e) => setEditing((prev) => ({ ...prev, nombre: e.target.value }))}
                    />
                  ) : s.nombre}
                </td>
                <td>
                  {editingId === s.id ? (
                    <input
                      className="w-20 rounded border px-2 py-1 text-sm"
                      value={editing.duracion}
                      onChange={(e) => setEditing((prev) => ({ ...prev, duracion: e.target.value }))}
                    />
                  ) : s.duracion_minutos}
                </td>
                <td>
                  {editingId === s.id ? (
                    <input
                      className="w-24 rounded border px-2 py-1 text-sm"
                      value={editing.precio}
                      onChange={(e) => setEditing((prev) => ({ ...prev, precio: e.target.value }))}
                    />
                  ) : s.precio}
                </td>
                <td className="text-right">
                  <div className="flex justify-end gap-2">
                    {editingId === s.id ? (
                      <Button
                        variant="secondary"
                        onClick={async () => {
                          try {
                            await serviciosService.update(s.id, {
                              nombre: sanitizeText(editing.nombre),
                              duracion_minutos: Number(editing.duracion),
                              precio: editing.precio,
                            });
                            setEditingId(null);
                            await refresh();
                            success('Servicio actualizado');
                          } catch {
                            error('No se pudo actualizar el servicio');
                          }
                        }}
                      >
                        Guardar
                      </Button>
                    ) : (
                      <Button variant="secondary" onClick={() => startEdit(s)}>Editar</Button>
                    )}
                    <Button
                      variant="danger"
                      onClick={async () => {
                        try {
                          await serviciosService.remove(s.id);
                          await refresh();
                          success('Servicio eliminado');
                        } catch {
                          error('No se pudo eliminar el servicio');
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
