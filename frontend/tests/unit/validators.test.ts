import { describe, expect, it } from 'vitest';
import { required, sanitizeText, validateEmail } from '../../src/utils/validators';

describe('validators', () => {
  it('sanitizeText removes angle brackets', () => {
    expect(sanitizeText('<script>hola</script>')).toBe('scripthola/script');
  });

  it('required validates empty text', () => {
    expect(required('', 'Nombre')).toBe('Nombre es requerido');
    expect(required('ok', 'Nombre')).toBeNull();
  });

  it('validateEmail works', () => {
    expect(validateEmail('bad-email')).toBe('Email no válido');
    expect(validateEmail('test@example.com')).toBeNull();
  });
});
