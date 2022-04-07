import { useEffect, useState } from 'react';
import { Stack, Grid, Typography,  } from '@mui/material';
import Colors from 'assets/colors';
import { Box } from '@mui/material';

const FunnyStack = ({ children, sx, ...props }) => (
    <Stack sx={{ p: 2, borderRadius: 2, border: 5, background: 'white', ...sx }} {...props}>
        {children}
    </Stack>
)

const Transaction = ({ recipient, reciever, amount }) => {
    return (
        <>
            <Stack direction="row" justifyContent="space-around">
                <Typography variant="h1">
                    {`User ${recipient}`}
                </Typography>
                <Typography variant="h1">
                    {`User ${reciever}`}
                </Typography>
                <Typography variant="h1" sx={{ color: Colors.green }}>
                    {`${amount} coins`}
                </Typography>
            </Stack>
            <Box sx={{ border: `2px dashed black` }}/>
        </>
    );
};

const getRandomInt = (max) => {
    return Math.floor(Math.random() * max);
}

const Transactions = () => {
    const [ listTransactions, setListTransactions ] = useState([]);

    useEffect(() => {
        const interval = setInterval(() => {
          const newList = [
                {
                    recipient: getRandomInt(5),
                    reciever: getRandomInt(5),
                    amount: getRandomInt(100)
                },
                ...listTransactions
          ];
          setListTransactions(newList);
        }, 1000);
        return () => clearInterval(interval);
    }, [listTransactions]);
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
            <Grid item xs={12}>
                <Stack direction="row" justifyContent="space-around">
                    <Typography variant="h1">
                        Recipient
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
                                recipient={transaction?.recipient}
                                reciever={transaction?.reciever}
                                amount={transaction?.amount}
                            />)}
                    </Stack>
                </Box>
            </Grid>
            <Grid item xs={12}>
                <Box sx={{ border: '4px dashed white' }}/>
            </Grid>
        </Grid>
    );
}

export default Transactions;