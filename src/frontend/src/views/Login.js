import { useContext } from 'react';
import { Box, Grid, Stack, Typography } from '@mui/material';
import Colors from 'assets/colors';
import { FormProvider, useForm } from 'react-hook-form';
import { AnimateButton, TextInput } from 'components';
import { LoadingButton } from '@mui/lab';
import { useSnackbar } from 'notistack';
import { UserContext } from 'context';
import Grow from '@mui/material/Grow';

const Login = () => {
    const methods = useForm();
    const { setIp } = useContext(UserContext);
    const { enqueueSnackbar } = useSnackbar();
    const onSubmit = ({ ip }) => {
        if (ip === undefined || ip === '') {
            enqueueSnackbar("IP is required", {
                preventDuplicate: true,
                variant: "error"
            });
        } 
        else {
            setIp(ip);
        }
    }
    return (
        <Box justifyContent="center" sx={{ display: 'flex', height: '100vh', width: '100%', background: Colors.purpleLight }}>
            <Grid container justifyContent="center" alignItems="center">
                <Grow in={true} timeout={1000}>
                    <Grid item xs={10} sm={6}>
                        <Typography variant="h2" sx={{ color: 'white' }}>NOOBCASH.</Typography>
                        <FormProvider {...methods}>
                            <Stack 
                                alignItems="center"
                                direction="row"
                                spacing={1}
                                sx={{ p: 4, background: 'white', boxShadow: 3, borderRadius: 1 }}
                            >
                                <TextInput id="ip" name="ip" placeholder="Your ip" />
                                <AnimateButton>
                                    {/* eslint-disable */}
                                    <LoadingButton 
                                        disableElevation
                                        fullWidth
                                        size="large"
                                        variant="contained"
                                        type="submit"
                                        onClick={methods.handleSubmit(onSubmit)}
                                    >
                                        LOGIN
                                    </LoadingButton>
                                </AnimateButton>
                            </Stack>
                        </FormProvider>
                    
                    
                    
                    
                    
                    
                    
                    
                    </Grid>
                </Grow>
            </Grid>
        </Box>
    );
}

export default Login;