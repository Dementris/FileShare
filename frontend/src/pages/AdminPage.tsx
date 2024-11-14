// src/pages/AdminPage.tsx
// src/pages/Admin.tsx
import React, { useState, useEffect } from 'react';
import {
    Container,
    Box,
    Typography,
    Paper,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Button,
    CircularProgress,
    Grid2,
    Grid
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import api from '../api/api.ts';

const AdminPage: React.FC = () => {
  const [adminInfo, setAdminInfo] = useState<any>(null);
  const [users, setUsers] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  // Fetch admin info and list of users when the component mounts
  useEffect(() => {
    const fetchAdminData = async () => {
      try {
        const [adminResponse, usersResponse] = await Promise.all([
          api.get('/users/me'),  // Get current logged-in user (admin)
          api.get('/users')      // Get list of all users
        ]);
        setAdminInfo(adminResponse.data);
        setUsers(usersResponse.data);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching data:', error);
        setLoading(false);
      }
    };

    fetchAdminData();
  }, []);

  // Handle logout
  const handleLogout = () => {
    localStorage.removeItem('accessToken');
    navigate('/login');
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh">
        <CircularProgress />
      </Box>
    );
  }

  return (
     <Container>
      {/* Admin Info Section */}
      <Box mt={4}>
        <Paper elevation={5} sx={{ padding: 3, backdropFilter: 'blur(12px)', borderRadius: 3, boxShadow: '0 8px 24px rgba(0, 0, 0, 0.2)' }}>
          <Typography variant="h3" gutterBottom sx={{ color: 'primary.main' }}>
            Admin Dashboard
          </Typography>
          {adminInfo ? (
            <Grid2 container spacing={4}>
              <Grid item xs={12} md={6}>
                <Typography variant="h6" sx={{ color: 'text.primary', marginBottom: 2 }}>Admin Info</Typography>
                <Typography variant="body1" sx={{ color: 'text.secondary' }}>Username: {adminInfo.username}</Typography>
                <Typography variant="body1" sx={{ color: 'text.secondary' }}>Email: {adminInfo.email}</Typography>
                <Typography variant="body1" sx={{ color: 'text.secondary' }}>Role: {adminInfo.role}</Typography>
                <Button variant="contained" color="secondary" onClick={handleLogout} sx={{ mt: 4 }}>
                  Logout
                </Button>
              </Grid>
            </Grid2>
          ) : (
            <Typography variant="h6" color="error">
              Could not load admin info.
            </Typography>
          )}
        </Paper>
      </Box>

      {/* User List Section */}
      <Box mt={6}>
        <Paper elevation={5} sx={{ padding: 3, backdropFilter: 'blur(12px)', borderRadius: 3, boxShadow: '0 8px 24px rgba(0, 0, 0, 0.2)' }}>
          <Typography variant="h3" gutterBottom sx={{ color: 'primary.main' }}>
            User List
          </Typography>
          <TableContainer component={Paper}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell sx={{ fontWeight: 'bold', color: 'text.primary' }}>Username</TableCell>
                  <TableCell sx={{ fontWeight: 'bold', color: 'text.primary' }}>Email</TableCell>
                  <TableCell sx={{ fontWeight: 'bold', color: 'text.primary' }}>Role</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {users.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={3} align="center">
                      No users found.
                    </TableCell>
                  </TableRow>
                ) : (
                  users.map((user) => (
                    <TableRow key={user.id}>
                      <TableCell sx={{ color: 'text.primary' }}>{user.username}</TableCell>
                      <TableCell sx={{ color: 'text.primary' }}>{user.email}</TableCell>
                      <TableCell sx={{ color: 'text.primary' }}>{user.role}</TableCell>
                    </TableRow>
                  ))
                )}
              </TableBody>
            </Table>
          </TableContainer>
        </Paper>
      </Box>
    </Container>
  );
};

export default AdminPage;

