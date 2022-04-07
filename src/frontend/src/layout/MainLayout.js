import { useContext, useEffect } from 'react';
import { UserContext } from 'context';
import { Box, Stack, Button, Typography, CircularProgress } from '@mui/material';
import { Outlet, useNavigate } from 'react-router-dom';
import { useWindowDimensions } from 'hooks';
import Colors from 'assets/colors';
import coin from 'assets/images/coin.png';

const DisplayBalance = ({ balance, status }) => {
    return {
        loading: <Typography variant="h1" sx={{ color: 'white', userSelect: 'none' }}>Loading...</Typography>,
        success: (
            <Stack direction="row" spacing={2} alignItems="center">
                <Typography variant="h2" sx={{ color: 'white', userSelect: 'none' }}>{balance}</Typography>
                <Box sx={{ width: 30, height: 30, backgroundImage: `url(${coin})`, backgroundSize: 'cover' }}/>
            </Stack>
        ),
        error: <Typography variant="h1" sx={{ color: 'white', userSelect: 'none' }}>Error :(</Typography>
    }[status];
}

const MainLayout = () => {
    const { height } = useWindowDimensions();
    const { setIP, balanceQuery } = useContext(UserContext);
    const navigate = useNavigate();
    const headerHeight = 75;
    const footerHeight = 75;

    return (
        <Box>
            {/* header */}
            <Box sx={{ position: 'absolute',  left: 0, top: 0, right: 0, height: headerHeight, borderBottom: 6, background: Colors.blue }}>
                <Box sx={{ display: 'flex', height: '100%' }}>
                    <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ pl: 2, pr: 2, width: '100%' }}>
                        <Box 
                            onClick={() => navigate("/home")}
                            sx={{ cursor: 'pointer' }}
                        >
                            <Typography variant="h1" sx={{ color: 'white', userSelect: 'none' }}>
                                NOOBCASH
                            </Typography>
                        </Box>
                        <Stack direction="row" spacing={1} alignItems="center" justifyContent="end">
                            <Typography variant="h1" sx={{ color: 'white' }}>
                                Your balance:
                            </Typography>
                            <Stack direction="row" spacing={1} sx={{ p: 1, borderRadius: 1, border: 5, background: Colors.green, cursor: 'pointer' }}>
                                {/* <Typography variant="h1" sx={{ color: 'white', userSelect: 'none' }}>
                                    {balanceQuery?.isLoading ? `- coins` : `${balanceQuery?.data?.balance} coins`}
                                </Typography>
                                <Typography variant="h1" sx={{ color: 'white', userSelect: 'none' }}>
                                    {balanceQuery?.isLoading ? `- coins` : `${balanceQuery?.data?.balance} coins`}
                                </Typography> */}
                                <DisplayBalance balance={balanceQuery?.data?.balance} status={balanceQuery.status} />
                            </Stack>
                        </Stack>
                        <Button
                            onClick={() => setIP(null)}
                            variant="contained"
                            color="secondary"
                        >
                            Logout
                        </Button>
                    </Stack>
                </Box>
            </Box>
            {/* body */}
            <Box sx={{ height: height - headerHeight - footerHeight, overflow: 'auto', mt: '75px', background: Colors.blueLight }}>
                <Outlet />
            </Box>
            {/* footer */}
            <Box sx={{ background: Colors.blue, borderTop: 6, position: 'absolute', left: 0, right: 0, bottom: 0, height: footerHeight }}>
                <Stack direction="row" alignItems="center" justifyContent="space-between" sx={{ p: 2 }}>
                    <Stack direction="row" spacing={2}>
                        <Typography variant="h1" sx={{ color: 'white' }}>
                                    el17838
                        </Typography>
                        <Typography variant="h1" sx={{ color: 'white' }}>
                                    el17083
                        </Typography>
                        <Typography variant="h1" sx={{ color: 'white' }}>
                                    el17140
                        </Typography>
                    </Stack>
                    <Box sx={{ width: 35, height: 35, backgroundImage: `url(${coin})`, backgroundSize: 'cover' }}/>
                    <Box sx={{ width: 35, height: 35, backgroundImage: `url(${coin})`, backgroundSize: 'cover' }}/>
                    <Box sx={{ width: 35, height: 35, backgroundImage: `url(${coin})`, backgroundSize: 'cover' }}/>
                    <Typography 
                        onClick={() => window.open("https://github.com/adonistseriotis/noobcash")}
                        variant="h1"
                        sx={{ color: 'white', textDecoration: 'underline', cursor: 'pointer' }}
                    >
                        Github repo
                    </Typography>
                </Stack>
            </Box>
        </Box>
    );
}

export default MainLayout;