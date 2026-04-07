import { NavLink } from 'react-router-dom';

const links = [
  { to: '/dashboard', label: 'Dashboard' },
  { to: '/agenda', label: 'Agenda' },
  { to: '/clientes', label: 'Clientes' },
  { to: '/servicios', label: 'Servicios' },
  { to: '/empleados', label: 'Empleados' },
  { to: '/configuracion', label: 'Configuración' },
];

export const Sidebar = () => (
  <aside className="hidden md:fixed md:inset-y-0 md:flex md:w-64 md:flex-col border-r bg-white">
    <div className="p-4 border-b">
      <h1 className="text-lg font-semibold">Booking SaaS</h1>
    </div>
    <nav className="p-3 space-y-1">
      {links.map((link) => (
        <NavLink
          key={link.to}
          to={link.to}
          className={({ isActive }) =>
            `block rounded-md px-3 py-2 text-sm ${isActive ? 'bg-brand-500 text-white' : 'hover:bg-slate-100'}`
          }
        >
          {link.label}
        </NavLink>
      ))}
    </nav>
  </aside>
);
