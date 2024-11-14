// src/components/Navbar.tsx
import React, {useEffect, useState} from 'react';
import {AppBar, Box, Button, CircularProgress, Toolbar, Typography} from '@mui/material';
import {Link, Navigate, useNavigate} from 'react-router-dom';
import api from "../api/api.ts";
import FileUploadPopup from "./FileUploadPopUp.tsx";


const Navbar: React.FC = () => {
    const [userInfo, setUserInfo] = useState<any>(null);
    const [loading, setLoading] = useState(true);


    const [open, setOpen] = useState(false);

    const handleOpen = () => setOpen(true);
    const handleClose = () => setOpen(false);

    const handleLogout = async () => {
        const response = await api.get("auth/logout")
        localStorage.removeItem("accessToke")
        localStorage.removeItem("refreshToken")
        if (response.status === 401){
            console.log("Error logout")
            return <Navigate to={"/unauthorized"}/>
        }
        else {
            window.location.replace("/")
        }
    }


    useEffect(() => {
        const fetchMe = async () => {
            try {
                const userResponse = await api.get('/users/me')
                setUserInfo(userResponse.data)
                setLoading(false)
            } catch (error) {
                console.error('Error fetching data:', error);
                setLoading(false)
            }
        };
        fetchMe();
    }, []);

    if (loading) {
        return (
            <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh">
                <CircularProgress/>
            </Box>
        );
    }
    return (
        <AppBar position="sticky">
            <Toolbar>
                <Typography variant="h6" sx={{flexGrow: 1}}>
                    FileShare
                </Typography>
                <Box>
                    <Button
                        component={Link}
                        to="/files"
                        color="inherit"
                        sx={{textTransform: 'none', marginRight: 2}}
                    >
                        Files
                    </Button>
                </Box>
                {userInfo.role == 'admin' && (
                    <Box>
                        <Button
                            component={Link}
                            to={"/admin"}
                            color="inherit"
                            sx={{textTransform: 'none', marginRight: 2}}
                        >
                            Admin Panel
                        </Button>
                    </Box>
                ) && (
                    <Box>
                        <Button variant="contained" color="primary" onClick={handleOpen}>
                            Upload File
                        </Button>
                        <FileUploadPopup open={open} onClose={handleClose}/>
                    </Box>
                )}
                {userInfo && (
                    <Box sx={{display: 'flex', alignItems: 'center', marginLeft: 3}}>
                        <Typography variant="body2" sx={{marginRight: 2}}>
                            {userInfo.username} ({userInfo.email})
                        </Typography>
                        <Box
                            sx={{
                                padding: '2px 8px',
                                backgroundColor: userInfo.role === 'admin' ? '#ff1500' : '#d512cf',
                                color: 'white',
                                borderRadius: '4px',
                                fontSize: '0.875rem',
                            }}
                        >
                            {userInfo.role}
                        </Box>
                    </Box>
                )}
                <Box>
                    <Button
                        color="inherit"
                        onClick={handleLogout}
                        sx={{textTransform: 'none', marginRight: 2}}>
                        Logout
                    </Button>
                </Box>

            </Toolbar>
        </AppBar>
    );
};

export default Navbar;

