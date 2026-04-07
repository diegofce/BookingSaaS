import { useMemo, useState } from 'react';
import { DashboardLayout } from '../components/layout/DashboardLayout';
import { AgendaCalendar } from '../components/agenda/AgendaCalendar';
import { CitaModal } from '../components/agenda/CitaModal';
import { useFetch } from '../hooks/useFetch';
import { citasService } from '../services/citasService';
import type { Cita } from '../types/cita';

export const AgendaPage = () => {
  const { data, loading, setData } = useFetch(citasService.getAll, []);
  const citas = useMemo(() => data || [], [data]);
  const [open, setOpen] = useState(false);
  const [selectedDate, setSelectedDate] = useState<string>();
  const [selectedCita, setSelectedCita] = useState<Cita | null>(null);

  const refresh = async () => {
    const next = await citasService.getAll();
    setData(next);
  };

  return (
    <DashboardLayout>
      {loading ? <p>Cargando agenda...</p> : null}
      <AgendaCalendar
        citas={citas}
        onSelectSlot={(date) => {
          setSelectedCita(null);
          setSelectedDate(date);
          setOpen(true);
        }}
        onSelectEvent={(cita) => {
          setSelectedCita(cita);
          setOpen(true);
        }}
      />

      <CitaModal
        open={open}
        initialDate={selectedDate}
        cita={selectedCita}
        onClose={() => setOpen(false)}
        onSave={async (payload) => {
          if (selectedCita) {
            await citasService.update(selectedCita.id, payload);
          } else {
            await citasService.create(payload);
          }
          await refresh();
        }}
        onDelete={async (id) => {
          await citasService.remove(id);
          await refresh();
        }}
      />
    </DashboardLayout>
  );
};
