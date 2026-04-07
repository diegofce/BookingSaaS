import { Input } from '../ui/Input';
import { Button } from '../ui/Button';

interface DateSelectorProps {
  date: string;
  loading: boolean;
  onDateChange: (date: string) => void;
  onLoadSlots: () => void;
}

export const DateSelector = ({ date, loading, onDateChange, onLoadSlots }: DateSelectorProps) => (
  <section className="space-y-2">
    <h2 className="text-lg font-semibold">2. Selecciona una fecha</h2>
    <div className="grid gap-2 sm:grid-cols-[1fr_auto]">
      <Input label="Fecha" type="date" value={date} onChange={(e) => onDateChange(e.target.value)} />
      <Button className="self-end" onClick={onLoadSlots} disabled={!date || loading}>
        {loading ? 'Cargando...' : 'Ver horarios'}
      </Button>
    </div>
  </section>
);
