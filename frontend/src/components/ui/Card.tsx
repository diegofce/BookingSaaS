import type { ReactNode } from 'react';

export const Card = ({ children }: { children: ReactNode }) => (
  <section className="rounded-xl border bg-white p-4 shadow-sm">{children}</section>
);
