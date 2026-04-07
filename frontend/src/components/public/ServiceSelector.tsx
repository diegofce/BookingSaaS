import type { ServicioPublico } from '../../types/public';
import { Card } from '../ui/Card';
import { Button } from '../ui/Button';
import { Loader } from '../ui/Loader';
import { Alert } from '../ui/Alert';

interface ServiceSelectorProps {
  servicios: ServicioPublico[];
  loading: boolean;
  error: string | null;
  selectedServiceId: number | null;
  onSelect: (servicio: ServicioPublico) => void;
}

export const ServiceSelector = ({ servicios, loading, error, selectedServiceId, onSelect }: ServiceSelectorProps) => {
  if (loading) return <Loader />;
  if (error) return <Alert message={error} />;
  if (!servicios.length) return <Alert type="error" message="No hay servicios disponibles por ahora." />;

  return (
    <div className="space-y-3">
      <h2 className="text-lg font-semibold">1. Selecciona un servicio</h2>
      <div className="grid gap-3 sm:grid-cols-2">
        {servicios.map((servicio) => {
          const isSelected = servicio.id === selectedServiceId;
          return (
            <Card key={servicio.id}>
              <div className="space-y-2">
                <h3 className="font-semibold">{servicio.nombre}</h3>
                <p className="text-sm text-slate-600">{servicio.descripcion || 'Servicio profesional'}</p>
                <div className="flex items-center justify-between text-sm">
                  <span className="text-slate-500">{servicio.duracion_minutos} min</span>
                  <span className="font-semibold">${servicio.precio}</span>
                </div>
                <Button
                  className="w-full"
                  variant={isSelected ? 'secondary' : 'primary'}
                  onClick={() => onSelect(servicio)}
                >
                  {isSelected ? 'Seleccionado' : 'Elegir servicio'}
                </Button>
              </div>
            </Card>
          );
        })}
      </div>
    </div>
  );
};
