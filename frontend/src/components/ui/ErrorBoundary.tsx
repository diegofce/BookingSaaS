import { Component, type ErrorInfo, type ReactNode } from 'react';

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(): State {
    return { hasError: true };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo): void {
    console.error('Unhandled UI error', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <main className="flex min-h-screen items-center justify-center bg-slate-100 p-4">
          <section className="max-w-md rounded-xl border bg-white p-6 text-center shadow-sm">
            <h1 className="text-xl font-semibold">Ocurrió un error inesperado</h1>
            <p className="mt-2 text-sm text-slate-600">Recarga la página para continuar.</p>
          </section>
        </main>
      );
    }

    return this.props.children;
  }
}
