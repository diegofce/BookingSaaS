import { useAuth } from '../../auth/useAuth';
import { Button } from '../ui/Button';

export const Navbar = () => {
  const { user, logout } = useAuth();

  return (
    <header className="sticky top-0 z-20 border-b bg-white px-4 py-3 md:px-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="font-medium">{user?.nombre || 'Usuario'}</p>
          <p className="text-sm text-slate-500 capitalize">{user?.rol}</p>
        </div>
        <Button onClick={logout} variant="secondary">Cerrar sesión</Button>
      </div>
    </header>
  );
};
