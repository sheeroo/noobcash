import { useContext, useEffect } from 'react';
import { Stack, Grid, Typography  } from '@mui/material';
import { UserContext } from 'context';
import Colors from 'assets/colors';
import { Box } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import socketio from 'socket.io-client';
const ENDPOINT = 'http://localhost:5000'

const FunnyStack = ({ children, sx, ...props }) => (
    <Stack sx={{ p: 2, borderRadius: 2, border: 5, background: 'white', ...sx }} {...props}>
        {children}
    </Stack>
)

const Home = () => {
    const { ip } = useContext(UserContext);
    const navigate = useNavigate();

    useEffect(() => {
        const socket = socketio(ENDPOINT);
        socket.on("hello", data => {
            console.log('DATA', data);
            alert('hello');
        });
      }, []);

    return (
        <Grid container spacing={2} sx={{ p: 2 }}>
            <Grid item xs={12}>
                <Stack direction="row" spacing={1} alignItems="center" justifyContent="end">
                    <Typography variant="h1">
                        Your balance:
                    </Typography>
                    <FunnyStack direction="row" spacing={1} sx={{ background: Colors.green, cursor: 'pointer' }}>
                        <Typography variant="h1" sx={{ color: 'white', userSelect: 'none' }}>
                            {`${125} coins`}
                        </Typography>
                    </FunnyStack>
                </Stack>
            </Grid>
            <Grid item xs={12}>
                <Box sx={{ border: '4px dashed white' }}/>
            </Grid>
            <Grid item xs={6}> 
                <FunnyStack>
                    <Typography variant="h1" noWrap>{`Welcome ${ip}`}</Typography>
                </FunnyStack>
            </Grid>
            <Grid item xs={6}>
                <FunnyStack>
                    <Typography variant="h1" noWrap>This is your noobCash client</Typography>
                </FunnyStack>
            </Grid>
            <Grid item xs={12}>
                <Box sx={{ border: '4px dashed white' }}/>
            </Grid>
            <Grid item xs={12}>
                <Box 
                    onClick={() => navigate("/transfer")}
                    sx={{ 
                        display: 'flex', 
                        justifyContent: "center", 
                        p: 5, 
                        background: Colors.yellowLight, 
                        border: 5, 
                        borderRadius: 2, 
                        cursor: 'pointer' 
                    }}
                >
                    <Typography variant="h1" sx={{ userSelect: 'none' }} noWrap>CLICK TO TRANSFER COINS</Typography>
                </Box>
            </Grid>
            <Grid item xs={12}>
                <Box sx={{ border: '4px dashed white' }}/>
            </Grid>
            <Grid item xs={12}>
                <Box 
                    onClick={() => navigate("/transactions")}
                    sx={{ 
                        display: 'flex', 
                        justifyContent: "center", 
                        p: 5, 
                        background: Colors.yellowLight, 
                        border: 5, 
                        borderRadius: 2, 
                        cursor: 'pointer' 
                    }}
                >
                    <Typography variant="h1" sx={{ userSelect: 'none' }} noWrap>CLICK TO WATCH TRANSACTION LOG</Typography>
                </Box>
            </Grid>
        </Grid>
    );
}

export default Home;