import { useState, memo, createContext, useEffect } from 'react';
import propTypes from 'prop-types';

const UserContext = createContext();

const UserProvider = memo(({ children }) => {
    const currentIp = localStorage.getItem("ip");
    const [ip, setIp] = useState(currentIp);
    useEffect(() => {
        if (ip === null) {
            localStorage.removeItem('ip');
        } else {
            localStorage.setItem('ip', ip);
        }
    }, [ip]);

    return <UserContext.Provider value={{ ip, setIp }}>{children}</UserContext.Provider>;
});

UserProvider.propTypes = {
    children: propTypes.node
};

export { UserProvider, UserContext };
