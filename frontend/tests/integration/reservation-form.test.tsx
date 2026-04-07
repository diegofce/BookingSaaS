import { fireEvent, render, screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import { ReservationForm } from '../../src/components/public/ReservationForm';

describe('ReservationForm', () => {
  it('renders and validates email visually', () => {
    const onChange = vi.fn();
    const onSubmit = vi.fn();
    render(
      <ReservationForm
        values={{ nombre: 'Juan', email: 'bad-email', telefono: '300' }}
        submitting={false}
        onChange={onChange}
        onSubmit={onSubmit}
      />
    );

    expect(screen.getByRole('alert')).toBeInTheDocument();
    fireEvent.click(screen.getByText('Confirmar reserva'));
    expect(onSubmit).not.toHaveBeenCalled();
  });
});
