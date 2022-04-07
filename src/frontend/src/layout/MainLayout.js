import { useContext } from 'react';
import { UserContext } from 'context';
import { Box, Stack, Button, Typography } from '@mui/material';
import { Outlet, useNavigate } from 'react-router-dom';
import { useWindowDimensions } from 'hooks';
import Colors from 'assets/colors';

const MainLayout = () => {
    const { height } = useWindowDimensions();
    const { setIp } = useContext(UserContext);
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
                                <Typography variant="h1" sx={{ color: 'white', userSelect: 'none' }}>
                                    {`${125} coins`}
                                </Typography>
                            </Stack>
                        </Stack>
                        <Button
                            onClick={() => setIp(null)}
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
            <Box sx={{ background: Colors.blue, borderTop: 6, position: 'absolute', left: 0, right: 0, bottom: 0, height: footerHeight }}/>
        </Box>
    );
}

export default MainLayout;