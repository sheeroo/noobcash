import { useEffect, useState, useContext } from 'react';
import { UserContext } from 'context';
import { Stack, Grid, Typography, Grow  } from '@mui/material';
import Colors from 'assets/colors';
import { Box } from '@mui/material';
import socketio from 'socket.io-client';
import coin from 'assets/images/coin.png';

const ENDPOINT = 'http://192.168.0.96:5000'

const FunnyStack = ({ children, sx, ...props }) => (
    <Stack sx={{ p: 2, borderRadius: 2, border: 5, background: 'white', ...sx }} {...props}>
        {children}
    </Stack>
)

const Transaction = ({ sender, receiver, amount }) => {
    return (
        <>
            <Stack direction="row" justifyContent="space-around">
                <Typography variant="h1">
                    {`User ${sender}`}
                </Typography>
                <Typography variant="h1">
                    {`User ${receiver}`}
                </Typography>
                <Stack direction="row" spacing={1} alignItems="center">
                    <Typography variant="h1" sx={{ color: Colors.green }}>
                        {amount}
                    </Typography>
                    <Box sx={{ width: 35, height: 35, backgroundImage: `url(${coin})`, backgroundSize: 'cover' }}/>
                </Stack>
            </Stack>
            <Box sx={{ border: `2px dashed black` }}/>
        </>
    );
};

const Transactions = () => {
    const [ listTransactions, setListTransactions ] = useState([]);
    const { ringQuery } = useContext(UserContext);

    useEffect(() => {
        const socket = socketio(ENDPOINT);
        socket.on("new_transaction", (newTransaction) => {
            console.log('ring', ringQuery.data);
            const sender = ringQuery.data.find((item) => item.address === newTransaction["sender_address"]).id;
            const receiver = ringQuery.data.find((item) => item.address === newTransaction["receiver_address"]).id;
            console.log('Sender', sender);
            console.log('Receiver', receiver);
            const newItem = {
                sender,
                receiver,
                amount: newTransaction.amount
            };
            setListTransactions(prev => ([newItem, ...prev]));
        });
    }, []);

    return (
        <Grid container spacing={2} sx={{ p: 2 }}>
            <Grid item xs={12}>
                <FunnyStack sx={{ background: Colors.yellowLight }}>
                    <Typography variant="h1" sx={{ color: Colors.yellow }}>
                                Transactions Log
                    </Typography>
                </FunnyStack>
            </Grid>
            <Grid item xs={12}>
                <Box sx={{ border: '4px dashed white' }}/>
            </Grid>
            <Grow in={true} timeout={1000}>
                <Grid item xs={12}>
                    <Stack direction="row" justifyContent="space-around">
                        <Typography variant="h1">
                            Sender
                        </Typography>
                        <Typography variant="h1">
                            Receiver
                        </Typography>
                        <Typography variant="h1">
                            Amount
                        </Typography>
                    </Stack>
                    <Box sx={{ p: 2, borderRadius: 2, height: 400, background: 'white', border: 5, overflowY: 'scroll' }}>
                        <Stack spacing={1}>
                            {listTransactions.map((transaction, key) => 
                                <Transaction 
                                    key={key}
                                    sender={transaction?.sender}
                                    receiver={transaction?.receiver}
                                    amount={transaction?.amount}
                                />)}
                        </Stack>
                    </Box>
                </Grid>
            </Grow>
            <Grid item xs={12}>
                <Box sx={{ border: '4px dashed white' }}/>
            </Grid>
        </Grid>
    );
}

export default Transactions;