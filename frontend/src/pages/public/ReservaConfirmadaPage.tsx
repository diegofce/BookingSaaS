import { Navigate, useParams } from 'react-router-dom';

export const ReservaConfirmadaPage = () => {
  const { dominio = '' } = useParams();
  return <Navigate to={`/agenda/${dominio}`} replace />;
};
