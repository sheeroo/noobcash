import { useContext, useState } from 'react';
import { UserContext } from 'context';
import { Stack, Grid, Typography, Button, Grow  } from '@mui/material';
import Colors from 'assets/colors';
import { Box } from '@mui/material';
import { FormProvider, useForm } from 'react-hook-form';
import { TextInput } from 'components';
import { newTransaction } from 'apis';
import { useSnackbar } from 'notistack';
import { useQueryClient } from 'react-query';
import useSound from 'use-sound';
import lostAudio from 'assets/audio/lost.mp3';
import coinAudio from 'assets/audio/coin.wav';

const FunnyStack = ({ children, sx, ...props }) => (
    <Stack sx={{ p: 2, borderRadius: 2, border: 5, background: 'white', ...sx }} {...props}>
        {children}
    </Stack>
)


const Transfer = () => {
    const methods = useForm();
    const queryClient = useQueryClient();
    const balanceData = queryClient.getQueryData('balance');
    const [isPlaying, setIsPlaying] = useState(false);
    const [playLost, playLostData] = useSound(lostAudio);
    const [playCoin, playCoinData] = useSound(coinAudio);

    const { enqueueSnackbar } = useSnackbar();
    const transactionRules = { 
        required: true,
        pattern: /^[0-9]+$/
    };


    const submitTransaction = async ({ receiver, amount }) => {
        try {
            const balance = balanceData.balance 
            await newTransaction({ receiver: parseInt(receiver), amount: parseInt(amount) });
            queryClient.invalidateQueries('balance');
            enqueueSnackbar("Your transaction was submitted", {
                variant: "success"
            })
            methods.reset({
                receiver: "",
                amount: ""
            });

            if (parseInt(amount) === balance) {
                setIsPlaying(true);
                playLost();
            } else {
                playCoin();
            }
        } catch (error) {
            enqueueSnackbar(error?.data?.message || "Something went wrong :(", {
                variant: "error"
            })
            console.error(error);
        }
    }

    return (
        <Grid container spacing={2} sx={{ p: 2 }}>
            <Grid item xs={12}>
                <FunnyStack sx={{ background: Colors.yellowLight }}>
                    <Typography variant="h1" sx={{ color: Colors.yellow }}>
                        Make a transaction
                    </Typography>
                </FunnyStack>
            </Grid>
            <Grid item xs={12}>
                <Box sx={{ border: '4px dashed white' }}/>
            </Grid>
            <Grow in={true} timeout={1200}>
                <Grid item xs={12}>
                    <FormProvider {...methods}>
                        <FunnyStack direction="row" spacing={1} alignItems="center">
                                <TextInput id="receiver" name="receiver" rules={transactionRules} placeholder="Receiver" />
                                <TextInput id="amount" name="amount" rules={transactionRules}placeholder="amount" />
                                <Button
                                    variant="contained"
                                    onClick={methods.handleSubmit(submitTransaction)}
                                >
                                    Go!
                                </Button>
                                {isPlaying && <Button
                                    variant="contained"
                                    color='secondary'
                                    onClick={() => { playLostData.stop(); setIsPlaying(false); }}
                                >
                                    STOP
                                </Button>}
                        </FunnyStack>
                    </FormProvider>
                </Grid>
            </Grow>
        </Grid>
    );
}

export default Transfer;