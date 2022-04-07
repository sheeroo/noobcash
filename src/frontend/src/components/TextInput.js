// mui
import { TextField, Typography } from '@mui/material';

// hook forms
import { useFormContext } from 'react-hook-form';

// prop-types
import PropTypes from 'prop-types';

const TextInput = (props) => {
    const { register, formState, control } = useFormContext();
    const { errors } = formState;
    const { name, rules, label, defaultValue, ...other } = props;

    return (
        <>
            <Typography>{label}</Typography>
            <TextField
                variant="outlined"
                inputProps={{
                    ...register(name, rules)
                }}
                InputLabelProps={{ shrink: true }}
                error={!!errors[name]}
                helperText={errors[name]?.message}
                required={rules?.required}
                size="small"
                fullWidth
                {...other}
            />
        </>
    );
};

TextInput.propTypes = {
    name: PropTypes.string.isRequired,
    label: PropTypes.string,
    rules: PropTypes.object
};

export default TextInput;
