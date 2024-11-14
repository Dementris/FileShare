// src/components/Footer.tsx
import React from 'react';
import { Box, Typography } from '@mui/material';

const Footer: React.FC = () => {
  return (
    <Box
      component="footer"
      sx={{
        backgroundColor: '#6200ea',
        padding: 2,
        marginTop: 'auto',
        textAlign: 'center',
      }}
    >
      <Typography variant="body2" color="white">
        © 2024 Your Company. All rights reserved.
      </Typography>
    </Box>
  );
};

export default Footer;
