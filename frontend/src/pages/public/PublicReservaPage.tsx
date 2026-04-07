import { Navigate, useParams } from 'react-router-dom';

export const PublicReservaPage = () => {
  const { dominio = '' } = useParams();
  return <Navigate to={`/agenda/${dominio}`} replace />;
};
