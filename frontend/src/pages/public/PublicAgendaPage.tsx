import { useEffect, useMemo, useState } from 'react';
import { useLocation, useParams } from 'react-router-dom';
import { PublicLayout } from '../../components/public/PublicLayout';
import { ServiceSelector } from '../../components/public/ServiceSelector';
import { DateSelector } from '../../components/public/DateSelector';
import { TimeSlots } from '../../components/public/TimeSlots';
import { ReservationForm } from '../../components/public/ReservationForm';
import { ReservaConfirmada } from '../../components/public/ReservaConfirmada';
import { Card } from '../../components/ui/Card';
import { Alert } from '../../components/ui/Alert';
import { agendaPublicaService } from '../../services/agendaPublicaService';
import type { DisponibilidadSlot, ReservaPayload, ServicioPublico } from '../../types/public';
import { validateEmail } from '../../utils/validators';

const buildSlots = (available: string[]): DisponibilidadSlot[] => {
  const base: DisponibilidadSlot[] = [];
  for (let hour = 8; hour <= 18; hour += 1) {
    ['00', '30'].forEach((minutes) => {
      if (hour === 18 && minutes === '30') return;
      const hourText = String(hour).padStart(2, '0');
      const slot = `${hourText}:${minutes}`;
      base.push({ hora: slot, disponible: available.includes(slot) });
    });
  }
  return base;
};

export const PublicAgendaPage = () => {
  const { dominio = '' } = useParams();
  const location = useLocation();

  const [loadingServicios, setLoadingServicios] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [servicios, setServicios] = useState<ServicioPublico[]>([]);

  const [selectedService, setSelectedService] = useState<ServicioPublico | null>(null);
  const [selectedDate, setSelectedDate] = useState('');
  const [loadingSlots, setLoadingSlots] = useState(false);
  const [slots, setSlots] = useState<DisponibilidadSlot[]>([]);
  const [selectedSlot, setSelectedSlot] = useState('');

  const [form, setForm] = useState({ nombre: '', email: '', telefono: '' });
  const [submitting, setSubmitting] = useState(false);
  const [confirmed, setConfirmed] = useState(false);

  const selectedServiceIdFromQuery = useMemo(
    () => Number(new URLSearchParams(location.search).get('servicio_id') || '0'),
    [location.search]
  );

  useEffect(() => {
    const load = async () => {
      try {
        setError(null);
        setLoadingServicios(true);
        const data = await agendaPublicaService.servicios(dominio);
        setServicios(data);
        if (selectedServiceIdFromQuery) {
          const preselected = data.find((s) => s.id === selectedServiceIdFromQuery);
          if (preselected) setSelectedService(preselected);
        }
      } catch (e: any) {
        setError(e?.response?.data?.detail || 'No se pudieron cargar los servicios');
      } finally {
        setLoadingServicios(false);
      }
    };

    load();
  }, [dominio, selectedServiceIdFromQuery]);

  const currentStep = useMemo(() => {
    if (confirmed) return 5;
    if (!selectedService) return 1;
    if (!selectedDate) return 2;
    if (!selectedSlot) return 3;
    return 4;
  }, [selectedService, selectedDate, selectedSlot, confirmed]);

  const loadAvailability = async () => {
    if (!selectedService || !selectedDate) {
      setError('Selecciona servicio y fecha');
      return;
    }

    try {
      setError(null);
      setLoadingSlots(true);
      const available = await agendaPublicaService.disponibilidad(dominio, selectedService.id, selectedDate);
      setSlots(buildSlots(available));
      setSelectedSlot('');
    } catch (e: any) {
      setError(e?.response?.data?.detail || 'No se pudo cargar disponibilidad');
    } finally {
      setLoadingSlots(false);
    }
  };

  const submitReservation = async () => {
    if (!selectedService || !selectedDate || !selectedSlot) {
      setError('Completa servicio, fecha y horario');
      return;
    }
    if (!form.nombre.trim() || !form.telefono.trim() || !form.email.trim()) {
      setError('Completa todos los datos del cliente');
      return;
    }
    if (validateEmail(form.email)) {
      setError('El email no es válido');
      return;
    }

    const payload: ReservaPayload = {
      servicio_id: selectedService.id,
      fecha: selectedDate,
      hora: selectedSlot,
      nombre: form.nombre.trim(),
      email: form.email.trim(),
      telefono: form.telefono.trim(),
    };

    try {
      setError(null);
      setSubmitting(true);
      await agendaPublicaService.reservar(dominio, payload);
      setConfirmed(true);
    } catch (e: any) {
      setError(e?.response?.data?.detail || 'No se pudo completar la reserva');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <PublicLayout
      negocioNombre={dominio}
      servicioSeleccionado={selectedService?.nombre}
    >
      <div className="mx-auto grid max-w-6xl gap-4 px-4 py-5 md:grid-cols-[340px_1fr]">
        <aside className="space-y-3">
          <Card>
            <h2 className="mb-2 text-sm font-semibold uppercase tracking-wide text-slate-500">Detalle</h2>
            {selectedService ? (
              <div className="space-y-2 text-sm">
                <p className="text-lg font-semibold">{selectedService.nombre}</p>
                <p className="text-slate-600">{selectedService.descripcion || 'Servicio profesional'}</p>
                <p><span className="font-medium">Duración:</span> {selectedService.duracion_minutos} minutos</p>
                <p><span className="font-medium">Precio:</span> ${selectedService.precio}</p>
              </div>
            ) : (
              <p className="text-sm text-slate-500">Selecciona un servicio para ver los detalles.</p>
            )}
          </Card>
          <Card>
            <h3 className="mb-2 text-sm font-semibold uppercase tracking-wide text-slate-500">Progreso</h3>
            <ol className="space-y-1 text-sm">
              <li className={currentStep >= 1 ? 'font-semibold text-brand-700' : 'text-slate-500'}>1. Servicio</li>
              <li className={currentStep >= 2 ? 'font-semibold text-brand-700' : 'text-slate-500'}>2. Fecha</li>
              <li className={currentStep >= 3 ? 'font-semibold text-brand-700' : 'text-slate-500'}>3. Horario</li>
              <li className={currentStep >= 4 ? 'font-semibold text-brand-700' : 'text-slate-500'}>4. Datos</li>
              <li className={currentStep >= 5 ? 'font-semibold text-emerald-700' : 'text-slate-500'}>5. Confirmación</li>
            </ol>
          </Card>
        </aside>

        <section className="space-y-4">
          {error ? <Alert message={error} /> : null}

          {!confirmed ? (
            <>
              <ServiceSelector
                servicios={servicios}
                loading={loadingServicios}
                error={null}
                selectedServiceId={selectedService?.id || null}
                onSelect={(servicio) => {
                  setSelectedService(servicio);
                  setSelectedDate('');
                  setSlots([]);
                  setSelectedSlot('');
                }}
              />

              {selectedService ? (
                <DateSelector
                  date={selectedDate}
                  loading={loadingSlots}
                  onDateChange={setSelectedDate}
                  onLoadSlots={loadAvailability}
                />
              ) : null}

              {selectedService && selectedDate ? (
                <TimeSlots slots={slots} selectedSlot={selectedSlot} onSelect={setSelectedSlot} />
              ) : null}

              {selectedService && selectedDate && selectedSlot ? (
                <ReservationForm
                  values={form}
                  submitting={submitting}
                  onChange={(name, value) => setForm((prev) => ({ ...prev, [name]: value }))}
                  onSubmit={submitReservation}
                />
              ) : null}
            </>
          ) : null}

          {confirmed && selectedService ? (
            <ReservaConfirmada servicio={selectedService} fecha={selectedDate} hora={selectedSlot} />
          ) : null}
        </section>
      </div>
    </PublicLayout>
  );
};
