import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../auth/useAuth';

export const PrivateRoute = () => {
  const { isAuthenticated, loading } = useAuth();
  if (loading) return <p className="p-4 text-sm text-slate-500">Validando sesión...</p>;
  return isAuthenticated ? <Outlet /> : <Navigate to="/login" replace />;
};
