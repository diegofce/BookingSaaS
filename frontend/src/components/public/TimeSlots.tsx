import type { DisponibilidadSlot } from '../../types/public';

interface TimeSlotsProps {
  slots: DisponibilidadSlot[];
  selectedSlot: string;
  onSelect: (hora: string) => void;
}

export const TimeSlots = ({ slots, selectedSlot, onSelect }: TimeSlotsProps) => (
  <section className="space-y-2">
    <h2 className="text-lg font-semibold">3. Selecciona un horario</h2>
    {slots.length ? (
      <div className="grid grid-cols-2 gap-2 sm:grid-cols-3">
        {slots.map((slot) => (
          <button
            key={slot.hora}
            type="button"
            disabled={!slot.disponible}
            onClick={() => onSelect(slot.hora)}
            className={`rounded-md border px-3 py-2 text-sm transition focus:outline-none focus:ring-2 focus:ring-brand-500 ${
              selectedSlot === slot.hora ? 'border-brand-500 bg-brand-50' : ''
            } ${!slot.disponible ? 'cursor-not-allowed border-slate-200 text-slate-400' : 'hover:bg-slate-50'}`}
          >
            {slot.hora}
          </button>
        ))}
      </div>
    ) : (
      <p className="text-sm text-slate-500">No hay horarios para la fecha seleccionada.</p>
    )}
  </section>
);
