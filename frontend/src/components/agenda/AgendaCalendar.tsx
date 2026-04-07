import FullCalendar from '@fullcalendar/react';
import dayGridPlugin from '@fullcalendar/daygrid';
import timeGridPlugin from '@fullcalendar/timegrid';
import interactionPlugin from '@fullcalendar/interaction';
import type { Cita } from '../../types/cita';

interface Props {
  citas: Cita[];
  onSelectSlot: (isoDate: string) => void;
  onSelectEvent: (cita: Cita) => void;
}

export const AgendaCalendar = ({ citas, onSelectSlot, onSelectEvent }: Props) => {
  const events = citas.map((c) => ({
    id: String(c.id),
    title: `Cita #${c.id}`,
    start: c.fecha_inicio,
    end: c.fecha_fin,
    color: c.estado === 'cancelada' ? '#dc2626' : '#2563eb',
  }));

  return (
    <FullCalendar
      plugins={[dayGridPlugin, timeGridPlugin, interactionPlugin]}
      initialView="timeGridWeek"
      events={events}
      selectable
      select={(info) => onSelectSlot(info.startStr)}
      eventClick={(info) => {
        const cita = citas.find((c) => c.id === Number(info.event.id));
        if (cita) onSelectEvent(cita);
      }}
      height="auto"
      locale="es"
    />
  );
};
