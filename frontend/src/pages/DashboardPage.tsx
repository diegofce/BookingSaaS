import { DashboardLayout } from '../components/layout/DashboardLayout';
import { Card } from '../components/ui/Card';
import { useFetch } from '../hooks/useFetch';
import { citasService } from '../services/citasService';
import { clientesService } from '../services/clientesService';
import { Loader } from '../components/ui/Loader';

export const DashboardPage = () => {
  const { data: citas, loading: loadingCitas } = useFetch(citasService.getAll, []);
  const { data: clientes, loading: loadingClientes } = useFetch(clientesService.getAll, []);

  return (
    <DashboardLayout>
      <div className="grid gap-4 md:grid-cols-3">
        <Card>
          <p className="text-sm text-slate-500">Próximas citas</p>
          <p className="text-2xl font-semibold">{loadingCitas ? '...' : citas?.length || 0}</p>
        </Card>
        <Card>
          <p className="text-sm text-slate-500">Clientes</p>
          <p className="text-2xl font-semibold">{loadingClientes ? '...' : clientes?.length || 0}</p>
        </Card>
        <Card>
          <p className="text-sm text-slate-500">Estado</p>
          <p className="text-2xl font-semibold text-emerald-600">Operativo</p>
        </Card>
      </div>
      {loadingCitas || loadingClientes ? <Loader /> : null}
    </DashboardLayout>
  );
};
