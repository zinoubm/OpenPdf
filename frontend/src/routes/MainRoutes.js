import { lazy } from 'react';

import Loadable from 'components/Loadable';
import MainLayout from 'layout/MainLayout';
import { Navigate } from 'react-router-dom';
import useAuth from 'api/hooks/useAuth';

const ChatingArea = Loadable(lazy(() => import('pages/Chat/index')));

const MainRoutes = () => {
  const { getToken } = useAuth();

  return {
    path: '/',
    element: getToken() ? <MainLayout /> : <Navigate to={'/home'} />,
    children: [
      {
        path: '/',
        element: <ChatingArea />
      }
    ]
  };
};

export default MainRoutes;
