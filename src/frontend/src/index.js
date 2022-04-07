import { ThemeProvider } from '@mui/material/styles';
import { createRoot } from 'react-dom/client';
import './index.css';
import { BrowserRouter } from "react-router-dom";
import Routes from 'routes';
import { SnackbarProvider } from 'notistack';
import { UserProvider } from 'context';
import theme from 'themes';
import { QueryClient, QueryClientProvider } from 'react-query'

const queryClient = new QueryClient();
const container = document.getElementById('root');
const root = createRoot(container);
root.render(
  <BrowserRouter>
    <ThemeProvider theme={theme}>
      <SnackbarProvider 
        maxSnack={1}
        anchorOrigin={{
          vertical: 'bottom',
          horizontal: 'center',
        }}
      >
          <UserProvider>
            <QueryClientProvider client={queryClient}>
              <Routes />
            </QueryClientProvider>
          </UserProvider>
      </SnackbarProvider>
    </ThemeProvider>
  </BrowserRouter>
);
