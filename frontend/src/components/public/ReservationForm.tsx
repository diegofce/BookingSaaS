import { useMemo } from 'react';
import { Input } from '../ui/Input';
import { Button } from '../ui/Button';
import { validateEmail } from '../../utils/validators';

interface ReservationFormValues {
  nombre: string;
  email: string;
  telefono: string;
}

interface ReservationFormProps {
  values: ReservationFormValues;
  submitting: boolean;
  onChange: (name: keyof ReservationFormValues, value: string) => void;
  onSubmit: () => void;
}

export const ReservationForm = ({ values, submitting, onChange, onSubmit }: ReservationFormProps) => {
  const emailError = useMemo(() => (values.email ? validateEmail(values.email) : null), [values.email]);

  return (
    <section className="space-y-2">
      <h2 className="text-lg font-semibold">4. Datos del cliente</h2>
      <div className="space-y-2">
        <Input label="Nombre" value={values.nombre} onChange={(e) => onChange('nombre', e.target.value)} required />
        <Input label="Email" type="email" value={values.email} onChange={(e) => onChange('email', e.target.value)} error={emailError} required />
        <Input label="Teléfono" value={values.telefono} onChange={(e) => onChange('telefono', e.target.value)} required />
      </div>
      <Button onClick={onSubmit} disabled={submitting || Boolean(emailError)} className="w-full sm:w-auto">
        {submitting ? 'Reservando...' : 'Confirmar reserva'}
      </Button>
    </section>
  );
};
