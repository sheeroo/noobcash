import { createTheme } from "@mui/material/styles";
import Colors from 'assets/colors';

const font =  "'Press Start 2P', cursive";

const theme = createTheme({
  typography: {
    fontFamily: font,
    h1: {
      fontWeight: 'bold',
      fontSize: '1rem',
      letterSpacing: '0.2rem',
      userSelect: 'none'
    },
    h2: {
      fontWeight: 'bold',
      fontSize: '1.2rem',
      letterSpacing: '0.2rem',
      userSelect: 'none'
    },
    h3: {
      fontWeight: 'bold',
      fontSize: '3rem',
      letterSpacing: '1rem',
      userSelect: 'none'
    }
  },
  palette: {
    primary: {
      main: Colors.purple,
      light: Colors.purpleLight
    },
    secondary: {
      main: Colors.yellow,
      light: Colors.yellowLight,
      contrastText: 'white'
    },
    error: {
      main: Colors.yellow,
      light: Colors.redLight
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
          root: {
            '&:hover': {
              background: Colors.yellow,
              boxShadow: 'none',
              '@media (hover: none)': {
                boxShadow: 'none',
              },
            },
            '&$focusVisible': {
                boxShadow: 'none',
            },
            '&:active': {
                boxShadow: 'none',
            },
            '&$disabled': {
                boxShadow: 'none',
            },
            boxShadow: 'none',
            fontWeight: 500,
            padding: 12,
            borderRadius: '2px'
          }
      }
    },
    MuiInputBase: {
      styleOverrides: {
        root: {
          padding: 3
        }
      }
    },
    MuiOutlinedInput: {
      styleOverrides: {
        root: {
          background: 'white',
          '.MuiOutlinedInput-notchedOutline': {
              border: '4px dashed',
              color: Colors.purple
          },
          '&:hover .MuiOutlinedInput-notchedOutline': {
              border: '4px dashed',
              color: Colors.yellow
          },
          "&.Mui-focused": {
            "& .MuiOutlinedInput-notchedOutline": {
              border: '4px dashed',
              color: Colors.yellow
            },
          }
        },
      }
    },
  }
});

export default theme;
