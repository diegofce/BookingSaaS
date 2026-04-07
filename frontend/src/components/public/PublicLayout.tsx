import type { ReactNode } from 'react';

interface PublicLayoutProps {
  negocioNombre: string;
  logoUrl?: string;
  servicioSeleccionado?: string;
  children: ReactNode;
}

export const PublicLayout = ({ negocioNombre, logoUrl, servicioSeleccionado, children }: PublicLayoutProps) => (
  <main className="min-h-screen bg-gradient-to-b from-slate-50 to-slate-100">
    <header className="border-b bg-white/95 backdrop-blur">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-3">
        <div className="flex items-center gap-3">
          <div className="flex h-9 w-9 items-center justify-center overflow-hidden rounded-full bg-brand-50 text-brand-700">
            {logoUrl ? <img src={logoUrl} alt={`Logo ${negocioNombre}`} className="h-full w-full object-cover" /> : negocioNombre.slice(0, 1).toUpperCase()}
          </div>
          <div>
            <p className="text-sm text-slate-500">Agenda online</p>
            <h1 className="text-lg font-semibold">{negocioNombre}</h1>
          </div>
        </div>
        <div className="text-right text-sm text-slate-600">
          <p className="font-medium">Servicio</p>
          <p>{servicioSeleccionado || 'Selecciona un servicio'}</p>
        </div>
      </div>
    </header>
    {children}
  </main>
);
