import type { ServicioPublico } from '../../types/public';

interface ReservaConfirmadaProps {
  servicio: ServicioPublico;
  fecha: string;
  hora: string;
}

export const ReservaConfirmada = ({ servicio, fecha, hora }: ReservaConfirmadaProps) => (
  <section className="rounded-xl border bg-white p-6 shadow-sm">
    <h2 className="text-2xl font-bold text-emerald-700">5. Reserva confirmada</h2>
    <p className="mt-2 text-slate-600">Tu cita fue registrada correctamente.</p>
    <div className="mt-4 space-y-1 text-sm">
      <p><span className="font-semibold">Servicio:</span> {servicio.nombre}</p>
      <p><span className="font-semibold">Fecha:</span> {fecha}</p>
      <p><span className="font-semibold">Hora:</span> {hora}</p>
    </div>
  </section>
);
