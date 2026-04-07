import { useState } from 'react';
import { DashboardLayout } from '../components/layout/DashboardLayout';
import { useFetch } from '../hooks/useFetch';
import { clientesService } from '../services/clientesService';
import { Button } from '../components/ui/Button';
import { Input } from '../components/ui/Input';
import { Card } from '../components/ui/Card';
import { sanitizeText } from '../utils/validators';
import { useToast } from '../state/useToast';
import type { Cliente } from '../types/cliente';

export const ClientesPage = () => {
  const { data, setData } = useFetch(clientesService.getAll, []);
  const { success, error } = useToast();
  const [nombre, setNombre] = useState('');
  const [email, setEmail] = useState('');
  const [telefono, setTelefono] = useState('');
  const [editingId, setEditingId] = useState<number | null>(null);
  const [editing, setEditing] = useState<{ nombre: string; email: string; telefono: string }>({
    nombre: '',
    email: '',
    telefono: '',
  });

  const refresh = async () => setData(await clientesService.getAll());
  const startEdit = (cliente: Cliente) => {
    setEditingId(cliente.id);
    setEditing({
      nombre: cliente.nombre,
      email: cliente.email || '',
      telefono: cliente.telefono || '',
    });
  };

  return (
    <DashboardLayout>
      <Card>
        <h2 className="mb-3 font-semibold">Nuevo cliente</h2>
        <div className="grid gap-2 md:grid-cols-4">
          <Input label="Nombre" value={nombre} onChange={(e) => setNombre(e.target.value)} />
          <Input label="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
          <Input label="Teléfono" value={telefono} onChange={(e) => setTelefono(e.target.value)} />
          <Button
            className="self-end"
            onClick={async () => {
              try {
                await clientesService.create({
                  nombre: sanitizeText(nombre),
                  email: sanitizeText(email),
                  telefono: sanitizeText(telefono),
                });
                setNombre('');
                setEmail('');
                setTelefono('');
                await refresh();
                success('Cliente creado');
              } catch {
                error('No se pudo crear el cliente');
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
              <th>Nombre</th><th>Email</th><th>Teléfono</th><th></th>
            </tr>
          </thead>
          <tbody>
            {(data || []).map((c) => (
              <tr key={c.id} className="border-t">
                <td>
                  {editingId === c.id ? (
                    <input
                      className="rounded border px-2 py-1 text-sm"
                      value={editing.nombre}
                      onChange={(e) => setEditing((prev) => ({ ...prev, nombre: e.target.value }))}
                    />
                  ) : c.nombre}
                </td>
                <td>
                  {editingId === c.id ? (
                    <input
                      className="rounded border px-2 py-1 text-sm"
                      value={editing.email}
                      onChange={(e) => setEditing((prev) => ({ ...prev, email: e.target.value }))}
                    />
                  ) : c.email}
                </td>
                <td>
                  {editingId === c.id ? (
                    <input
                      className="rounded border px-2 py-1 text-sm"
                      value={editing.telefono}
                      onChange={(e) => setEditing((prev) => ({ ...prev, telefono: e.target.value }))}
                    />
                  ) : c.telefono}
                </td>
                <td className="text-right">
                  <div className="flex justify-end gap-2">
                    {editingId === c.id ? (
                      <Button
                        variant="secondary"
                        onClick={async () => {
                          try {
                            await clientesService.update(c.id, {
                              nombre: sanitizeText(editing.nombre),
                              email: sanitizeText(editing.email),
                              telefono: sanitizeText(editing.telefono),
                            });
                            setEditingId(null);
                            await refresh();
                            success('Cliente actualizado');
                          } catch {
                            error('No se pudo actualizar el cliente');
                          }
                        }}
                      >
                        Guardar
                      </Button>
                    ) : (
                      <Button variant="secondary" onClick={() => startEdit(c)}>Editar</Button>
                    )}
                    <Button
                      variant="danger"
                      onClick={async () => {
                        try {
                          await clientesService.remove(c.id);
                          await refresh();
                          success('Cliente eliminado');
                        } catch {
                          error('No se pudo eliminar el cliente');
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
