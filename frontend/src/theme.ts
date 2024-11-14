import { createTheme } from "@mui/material";

const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#9c27b0',
      light: '#bb66cc',
    },
    secondary: {
      main: '#6200ea',
      light: '#bb6eed',
    },
    text: {
      primary: '#ffffff',
      secondary: '#e0e0e0',
    },
    background: {
      default: '#121212',
      paper: 'linear-gradient(135deg, rgba(0, 0, 0, 0.85) 0%, rgba(0, 0, 0, 0.95) 100%)', // More balanced dark gradient for paper
    },
  },
  typography: {
    fontFamily: '"Roboto", sans-serif',
    h1: {
      fontWeight: 700,
      fontSize: '2.25rem',
      letterSpacing: '0.5px',
      lineHeight: 1.2,
    },
    h2: {
      fontWeight: 600,
      fontSize: '1.75rem',
      lineHeight: 1.3,
    },
    h3: {
      fontWeight: 500,
      fontSize: '1.5rem',
      lineHeight: 1.4,
    },
    body1: {
      fontSize: '1rem',
      lineHeight: 1.6,
    },
    body2: {
      padding: '10px',
      fontSize: '0.875rem',
      lineHeight: 1.6,
      backgroundColor: '#6200ea',
      boxShadow: '0 8px 16px rgba(255, 0, 255, 0.5)',
      transform: 'scale(1.05)',
    },
  },
  components: {
     MuiCssBaseline: {
      styleOverrides: {
        body: {
          scrollbarColor: '#6200ea #121212',
          scrollbarWidth: 'thin',
          '&::-webkit-scrollbar': {
            width: '8px',
            height: '8px',
          },
          '&::-webkit-scrollbar-thumb': {
            backgroundColor: '#9c27b0',
            borderRadius: '4px',
            border: '2px solid transparent',
            backgroundClip: 'padding-box',
          },
          '&::-webkit-scrollbar-thumb:hover': {
            backgroundColor: '#9c27b0',
          },
          '&::-webkit-scrollbar-track': {
            backgroundColor: '#121212',
            borderRadius: '4px',
          },
        },
      },
    },
    MuiTableCell: {
      styleOverrides: {
        root: {
          padding: '16px',
          color: '#e0e0e0',
          borderBottom: '1px solid #444', // Subtle borders for table cells
        },
      },
    },
    MuiTableHead: {
      styleOverrides: {
        root: {
          backgroundColor: '#363139', // Purple background for header
          borderBottom: '2px solid #9c27b0', // Border between header and rows
        },
      },
    },
    MuiTableRow: {
      styleOverrides: {
        root: {
          '&:hover': {
            backgroundColor: '#333', // Hover effect for rows
          },
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: '12px',
          padding: '12px 24px',
          fontWeight: 'bold',
          fontSize: '1rem',
          textTransform: 'none',
          boxShadow: '0 4px 8px rgba(255, 0, 255, 0.2)',
          transition: 'all 0.3s ease-in-out',
          '&:hover': {
            backgroundColor: '#6200ea',
            boxShadow: '0 8px 16px rgba(255, 0, 255, 0.5)',
            transform: 'scale(1.05)',
          },
          '&:active': {
            backgroundColor: '#9c27b0',
            transform: 'scale(1)',
            boxShadow: '0 6px 12px rgba(255, 0, 255, 0.3)',
          },
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          background: 'linear-gradient(135deg, rgba(0, 0, 0, 0.85) 0%, rgba(0, 0, 0, 0.95) 100%)',
          backdropFilter: 'blur(8px)',
          borderRadius: '16px',
          padding: '24px',
          boxShadow: '0 8px 24px rgba(0, 0, 0, 0.4)',
          border: '1px solid #444', // Light border for cards
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: '16px',
          padding: '16px',
          boxShadow: '0 4px 12px rgba(0, 0, 0, 0.5)', // Subtle shadow for cards
          border: '1px solid #444', // Adding border for cards
        },
      },
    },
  },
});

export default theme;

