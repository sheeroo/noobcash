import { Stack, Grid, Typography, Button  } from '@mui/material';
import Colors from 'assets/colors';
import { Box } from '@mui/material';
import { FormProvider, useForm } from 'react-hook-form';
import { TextInput } from 'components';

const FunnyStack = ({ children, sx, ...props }) => (
    <Stack sx={{ p: 2, borderRadius: 2, border: 5, background: 'white', ...sx }} {...props}>
        {children}
    </Stack>
)

const Transfer = () => {
    const methods = useForm();
    const transactionRules = { 
        required: true,
        pattern: /^[0-9]+$/
    };
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
            <Grid item xs={12}>
                <FormProvider {...methods}>
                    <FunnyStack direction="row" spacing={1} alignItems="center">
                            <TextInput id="targetIndex" name="targetIndex" rules={transactionRules} placeholder="Reciever" />
                            <TextInput id="amount" name="amount" rules={transactionRules}placeholder="amount" />
                            <Button
                                variant="contained"
                                onClick={methods.handleSubmit((values) => {
                                    console.log('values', values);
                                })}
                            >
                                Go!
                            </Button>
                    </FunnyStack>
                </FormProvider>
            </Grid>
        </Grid>
    );
}

export default Transfer;