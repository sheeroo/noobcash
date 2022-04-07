import { useContext } from 'react';
import { UserContext } from 'context';
import { Stack, Grid, Typography, Button, Grow  } from '@mui/material';
import Colors from 'assets/colors';
import { Box } from '@mui/material';
import { FormProvider, useForm } from 'react-hook-form';
import { TextInput } from 'components';
import { newTransaction } from 'apis';
import { useSnackbar } from 'notistack';
import { useQueryClient } from 'react-query';

const FunnyStack = ({ children, sx, ...props }) => (
    <Stack sx={{ p: 2, borderRadius: 2, border: 5, background: 'white', ...sx }} {...props}>
        {children}
    </Stack>
)


const Transfer = () => {
    const methods = useForm();
    const queryClient = useQueryClient();

    const { enqueueSnackbar } = useSnackbar();
    const transactionRules = { 
        required: true,
        pattern: /^[0-9]+$/
    };

    const submitTransaction = async ({ receiver, amount }) => {
        try {
            await newTransaction({ receiver: parseInt(receiver), amount: parseInt(amount) });
            queryClient.invalidateQueries('balance');
            enqueueSnackbar("Your transaction was submitted", {
                variant: "success"
            })
            methods.reset({
                receiver: "",
                amount: ""
            })
        } catch (error) {
            enqueueSnackbar(error?.data?.message || "Something went wrong :(", {
                variant: "error"
            })
            console.error(error?.data.message);
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
                        </FunnyStack>
                    </FormProvider>
                </Grid>
            </Grow>
        </Grid>
    );
}

export default Transfer;