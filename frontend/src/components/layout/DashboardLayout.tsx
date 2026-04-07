import type { ReactNode } from 'react';
import { Sidebar } from './Sidebar';
import { Navbar } from './Navbar';

interface Props {
  children: ReactNode;
}

export const DashboardLayout = ({ children }: Props) => (
  <div className="min-h-screen bg-slate-100">
    <Sidebar />
    <div className="md:pl-64">
      <Navbar />
      <main className="p-4 md:p-6">{children}</main>
    </div>
  </div>
);
