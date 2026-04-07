import { useState } from 'react';
import { Modal } from '../ui/Modal';
import { Input } from '../ui/Input';
import { Button } from '../ui/Button';
import type { Cita } from '../../types/cita';

interface Props {
  open: boolean;
  initialDate?: string;
  cita?: Cita | null;
  onClose: () => void;
  onSave: (payload: { cliente_id: number; servicio_id: number; fecha_inicio: string; monto_pagado: string }) => Promise<void>;
  onDelete?: (id: number) => Promise<void>;
}

export const CitaModal = ({ open, onClose, onSave, onDelete, cita, initialDate }: Props) => {
  const [clienteId, setClienteId] = useState<string>(cita ? String(cita.cliente_id) : '');
  const [servicioId, setServicioId] = useState<string>(cita ? String(cita.servicio_id) : '');
  const [fechaInicio, setFechaInicio] = useState<string>((cita?.fecha_inicio || initialDate || '').slice(0, 16));

  const submit = async () => {
    await onSave({
      cliente_id: Number(clienteId),
      servicio_id: Number(servicioId),
      fecha_inicio: new Date(fechaInicio).toISOString(),
      monto_pagado: cita?.monto_pagado || '0.00',
    });
    onClose();
  };

  return (
    <Modal open={open} title={cita ? 'Editar cita' : 'Crear cita'} onClose={onClose}>
      <div className="space-y-3">
        <Input label="Cliente ID" value={clienteId} onChange={(e) => setClienteId(e.target.value)} />
        <Input label="Servicio ID" value={servicioId} onChange={(e) => setServicioId(e.target.value)} />
        <Input label="Fecha inicio" type="datetime-local" value={fechaInicio} onChange={(e) => setFechaInicio(e.target.value)} />
        <div className="flex gap-2">
          <Button onClick={submit}>Guardar</Button>
          {cita && onDelete ? (
            <Button
              variant="danger"
              onClick={async () => {
                await onDelete(cita.id);
                onClose();
              }}
            >
              Cancelar cita
            </Button>
          ) : null}
        </div>
      </div>
    </Modal>
  );
};
