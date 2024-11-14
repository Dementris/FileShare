import React from 'react';
import { Container, Box, Typography, Button } from '@mui/material';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import {Link} from 'react-router-dom';

const RegistrationSuccessPage: React.FC = () => {
  return (
    <Container maxWidth="sm">
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          height: '100vh',
          textAlign: 'center',
        }}
      >
        {/* Success Icon */}
        <CheckCircleIcon
          sx={{
            fontSize: 60,
            color: 'green',
            marginBottom: 2,
          }}
        />
        <Typography variant="h4" component="h1" gutterBottom>
          Registration Successful!
        </Typography>
        <Typography variant="body1" paragraph>
          Thank you for registering with us. Your account has been created successfully.
        </Typography>
        <Typography variant="body2" paragraph>
          You can now proceed to log in and access your dashboard.
        </Typography>
        <Button
          variant="contained"
          color="primary"
          component={Link}
          to="/login"
          sx={{ marginTop: '20px' }}
        >
          Go to Login
        </Button>
      </Box>
    </Container>
  );
};

export default RegistrationSuccessPage;
