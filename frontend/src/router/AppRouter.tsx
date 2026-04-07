import { Navigate, Route, Routes } from 'react-router-dom';
import { PrivateRoute } from './PrivateRoute';
import { LoginPage } from '../pages/LoginPage';
import { DashboardPage } from '../pages/DashboardPage';
import { AgendaPage } from '../pages/AgendaPage';
import { ClientesPage } from '../pages/ClientesPage';
import { ServiciosPage } from '../pages/ServiciosPage';
import { EmpleadosPage } from '../pages/EmpleadosPage';
import { ConfiguracionPage } from '../pages/ConfiguracionPage';
import { PublicAgendaPage } from '../pages/public/PublicAgendaPage';
import { PublicReservaPage } from '../pages/public/PublicReservaPage';
import { ReservaConfirmadaPage } from '../pages/public/ReservaConfirmadaPage';

export const AppRouter = () => (
  <Routes>
    <Route path="/login" element={<LoginPage />} />
    <Route path="/agenda/:dominio" element={<PublicAgendaPage />} />
    <Route path="/agenda/:dominio/reservar" element={<PublicReservaPage />} />
    <Route path="/agenda/:dominio/confirmada" element={<ReservaConfirmadaPage />} />

    <Route element={<PrivateRoute />}>
      <Route path="/dashboard" element={<DashboardPage />} />
      <Route path="/agenda" element={<AgendaPage />} />
      <Route path="/clientes" element={<ClientesPage />} />
      <Route path="/servicios" element={<ServiciosPage />} />
      <Route path="/empleados" element={<EmpleadosPage />} />
      <Route path="/configuracion" element={<ConfiguracionPage />} />
    </Route>

    <Route path="*" element={<Navigate to="/dashboard" replace />} />
  </Routes>
);
