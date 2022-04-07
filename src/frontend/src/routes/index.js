import { memo } from 'react';
import { useRoutes } from 'react-router-dom';

// routes
import { useContext } from 'react';
import MainRoutes from './MainRoutes';
import AuthenticationRoutes from './AuthenticationRoutes';
import { UserContext } from 'context';

// ==============================|| APP ROOT ||============================== //

const Routes = memo(() => {
    const { myIP } = useContext(UserContext);
    const routes = myIP ? MainRoutes() : AuthenticationRoutes();
    return useRoutes(routes, '');
});

export default Routes;
