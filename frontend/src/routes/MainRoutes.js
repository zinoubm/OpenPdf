import { lazy } from 'react';

// project import
import Loadable from 'components/Loadable';
import MainLayout from 'layout/MainLayout';
// import PrivateRoutes from './PrivateRoutes';
import { Navigate } from 'react-router-dom';
import useAuth from 'api/hooks/useAuth';

// render - dashboard
const DashboardDefault = Loadable(lazy(() => import('pages/dashboard')));
const ChatingArea = Loadable(lazy(() => import('pages/Chat/index')));

// render - sample page
const SamplePage = Loadable(lazy(() => import('pages/extra-pages/SamplePage')));

// render - utilities
const Typography = Loadable(lazy(() => import('pages/components-overview/Typography')));
const Color = Loadable(lazy(() => import('pages/components-overview/Color')));
const Shadow = Loadable(lazy(() => import('pages/components-overview/Shadow')));
const AntIcons = Loadable(lazy(() => import('pages/components-overview/AntIcons')));

// ==============================|| MAIN ROUTING ||============================== //

const MainRoutes = () => {
  const { getToken } = useAuth();

  return {
    path: '/',
    element: getToken() ? <MainLayout /> : <Navigate to={'/login'} />,
    children: [
      {
        path: '/',
        element: <ChatingArea />
      },
      {
        path: 'color',
        element: <Color />
      },
      {
        path: 'dashboard',
        children: [
          {
            path: 'default',
            element: <DashboardDefault />
          }
        ]
      },
      {
        path: 'sample-page',
        element: <SamplePage />
      },
      {
        path: 'shadow',
        element: <Shadow />
      },
      {
        path: 'typography',
        element: <Typography />
      },
      {
        path: 'icons/ant',
        element: <AntIcons />
      }
    ]
  };
};

export default MainRoutes;
