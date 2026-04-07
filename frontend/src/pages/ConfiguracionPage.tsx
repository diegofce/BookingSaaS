import { useState } from 'react';
import { DashboardLayout } from '../components/layout/DashboardLayout';
import { Card } from '../components/ui/Card';
import { Input } from '../components/ui/Input';
import { Button } from '../components/ui/Button';

export const ConfiguracionPage = () => {
  const [recordatorioMin, setRecordatorioMin] = useState('60');

  return (
    <DashboardLayout>
      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <h2 className="mb-2 font-semibold">Horarios negocio</h2>
          <p className="text-sm text-slate-600">Gestiona los horarios en el módulo Agenda / API de horarios.</p>
        </Card>
        <Card>
          <h2 className="mb-2 font-semibold">Recordatorios</h2>
          <Input label="Minutos antes" value={recordatorioMin} onChange={(e) => setRecordatorioMin(e.target.value)} />
          <div className="mt-2">
            <Button type="button">Guardar (UI)</Button>
          </div>
          <p className="mt-2 text-xs text-slate-500">Nota: backend actual maneja esta configuración por variables de entorno.</p>
        </Card>
      </div>
    </DashboardLayout>
  );
};
