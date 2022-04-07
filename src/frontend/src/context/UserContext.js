import { useState, memo, createContext, useEffect } from 'react';
import propTypes from 'prop-types';
import { useQuery, useQueryClient } from 'react-query';
import { getBalance, getRing } from 'apis';
import socketio from 'socket.io-client';

const UserContext = createContext();
const ENDPOINT = 'http://192.168.0.96:5000'

const UserProvider = memo(({ children }) => {
    const currentIp = localStorage.getItem("ip");
    const [myIP, setIP] = useState(currentIp);
    const [whoami, setWhoami] = useState(null);
    const balanceQuery = useQuery('balance', async () => await getBalance(), { enabled: !!myIP });
    const ringQuery = useQuery('ring', async () => await getRing(), { enabled: !!myIP });
    const queryClient = useQueryClient();

    useEffect(() => {
        // cheap work around to refresh our balance
        const socket = socketio(ENDPOINT);
        socket.on("new_transaction", () => {
            console.log('new transaction');
            queryClient.invalidateQueries('balance');
        });
    }, [])
    useEffect(() => {
        if (ringQuery.status === 'success') {
            const myPort = parseInt(myIP.slice(-4));
            const _whoami = ringQuery?.data?.find((item) => item.port === myPort).id;
            setWhoami(_whoami);
        }
    }, [ringQuery.status])

    useEffect(() => {
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
