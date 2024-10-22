import { lazy } from 'react';

// project import
import Loadable from 'components/Loadable';
import MinimalLayout from 'layout/MinimalLayout';

// render - login
const AuthLogin = Loadable(lazy(() => import('pages/authentication/Login')));
const AuthRegister = Loadable(lazy(() => import('pages/authentication/Register')));
import LandingPage from 'pages/landingPage/index';
import VerifyEmail from 'pages/verify/index';
import Verified from 'pages/verify/verified';

// ==============================|| AUTH ROUTING ||============================== //

const LoginRoutes = {
  path: '/',
  element: <MinimalLayout />,
  children: [
    {
      path: 'login',
      element: <AuthLogin />
    },
    {
      path: 'register',
      element: <AuthRegister />
    },
    {
      path: 'home',
      element: <LandingPage />
    },
    {
      path: 'verify',
      element: <VerifyEmail />
    },
    {
      path: 'verified',
      element: <Verified />
    }
  ]
};

export default LoginRoutes;
