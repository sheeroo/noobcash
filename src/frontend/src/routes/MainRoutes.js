import { lazy } from 'react';
import { Navigate } from 'react-router-dom';

// project imports
import Loadable from 'components/Loadable';

// dashboard routing
const Home = Loadable(lazy(() => import('views/Home')));
const Transactions = Loadable(lazy(() => import('views/Transactions')));
const Transfer = Loadable(lazy(() => import('views/Transfer')));
const MainLayout = Loadable(lazy(() => import('layout/MainLayout')));

// ==============================|| MAIN ROUTING ||============================== //

const MainRoutes = () => ([
    {
        path: '',
        element: <MainLayout />,
        children: [
            {
                path: 'home',
                element: <Home />
            },
            {
                path: 'transactions',
                element: <Transactions />
            },
            {
                path: 'transfer',
                element: <Transfer />
            },
            {
                path: '*',
                element: <Navigate to="home" />
            }
        ]
    }
]);

export default MainRoutes;
