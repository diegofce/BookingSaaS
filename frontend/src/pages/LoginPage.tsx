import { useState } from 'react';
import type { FormEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../auth/useAuth';
import { Input } from '../components/ui/Input';
import { Button } from '../components/ui/Button';
import { Card } from '../components/ui/Card';
import { Alert } from '../components/ui/Alert';
import { validateEmail } from '../utils/validators';

export const LoginPage = () => {
  const { login, loading } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [negocioId, setNegocioId] = useState('1');
  const [error, setError] = useState<string | null>(null);

  const onSubmit = async (e: FormEvent) => {
    e.preventDefault();
    const emailErr = validateEmail(email);
    if (emailErr) {
      setError(emailErr);
      return;
    }

    try {
      setError(null);
      await login({ email, password, negocio_id: Number(negocioId) });
      navigate('/dashboard');
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Credenciales inválidas');
    }
  };

  return (
    <main className="flex min-h-screen items-center justify-center bg-gradient-to-br from-slate-100 to-blue-100 p-4">
      <Card>
        <h1 className="mb-4 text-xl font-semibold">Iniciar sesión</h1>
        <form onSubmit={onSubmit} className="w-80 space-y-3">
          {error ? <Alert message={error} /> : null}
          <Input label="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
          <Input label="Password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
          <Input label="Negocio ID" value={negocioId} onChange={(e) => setNegocioId(e.target.value)} />
          <Button type="submit" disabled={loading} className="w-full">Entrar</Button>
        </form>
      </Card>
    </main>
  );
};
