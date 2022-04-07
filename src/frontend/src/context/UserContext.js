import { useState, memo, createContext, useEffect } from 'react';
import propTypes from 'prop-types';
import { useQuery } from 'react-query';
import { getBalance, getRing } from 'apis';

const UserContext = createContext();

const UserProvider = memo(({ children }) => {
    const currentIp = localStorage.getItem("ip");
    const [myIP, setIP] = useState(currentIp);
    const [whoami, setWhoami] = useState(null);
    const balanceQuery = useQuery('balance', async () => await getBalance(), { enabled: !!myIP });
    const ringQuery = useQuery('ring', async () => await getRing(), { enabled: !!myIP });

    useEffect(() => {
        if (ringQuery.status === 'success') {
            const myPort = parseInt(myIP.slice(-4));
            const _whoami = ringQuery?.data?.find((item) => item.port === myPort).id;
            setWhoami(_whoami);
        }
    }, [ringQuery.status])

    useEffect(() => {
        console.log("iam here");
        // user set ip to null, we need to dispatch remove because
        // it will be set as "null"
        if (myIP === null) {
            localStorage.removeItem('ip');
        } else {
            localStorage.setItem('ip', myIP);
        }
    }, [myIP]);

    return <UserContext.Provider value={{ whoami, myIP, setIP, balanceQuery, ringQuery }}>{children}</UserContext.Provider>;
});

UserProvider.propTypes = {
    children: propTypes.node
};

export { UserProvider, UserContext };
