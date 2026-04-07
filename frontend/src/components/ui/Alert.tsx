export const Alert = ({ message, type = 'error' }: { message: string; type?: 'error' | 'success' }) => (
  <div
    role="alert"
    className={`rounded-md px-3 py-2 text-sm ${
      type === 'error' ? 'bg-red-50 text-red-700' : 'bg-emerald-50 text-emerald-700'
    }`}
  >
    {message}
  </div>
);
