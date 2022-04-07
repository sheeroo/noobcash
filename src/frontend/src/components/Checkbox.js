import { Checkbox, FormControlLabel, Typography, Stack } from '@mui/material';
import PropTypes from 'prop-types';
import { useFormContext, useController } from 'react-hook-form';

const FormCheckbox = ({ name, label, ...other }) => {
    const { control } = useFormContext();
    const { field, fieldState } = useController({ name, control });

    return (
        <Stack>
            <FormControlLabel
                control={
                    /* eslint-disable */
                    <Checkbox
                        checked={field.value}
                        onChange={field.onChange}
                        name={field.name}
                        {...other}
                    />
                }
                label={<Typography variant="subtitle1">{label}</Typography>}
            />
            {!!fieldState.error && <Typography variant="error">{fieldState.error?.message}</Typography>}
        </Stack>
    );
};

FormCheckbox.propTypes = {
    name: PropTypes.string.isRequired,
    label: PropTypes.string
}

export default FormCheckbox;
