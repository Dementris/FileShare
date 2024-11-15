import React, {useEffect, useState} from 'react';
import {Navigate} from 'react-router-dom';
import {jwtDecode} from 'jwt-decode';
import axios from 'axios';
import {CircularProgress} from "@mui/material";

interface TokenPayload {
    exp: number;
    role: string;
}

interface ProtectedRouteProps {
    children: JSX.Element;
    requiredRole: 'A' | 'U';
}


const isTokenExpired = (token: string): boolean => {
    try {
        const {exp} = jwtDecode<TokenPayload>(token);
        return Date.now() >= exp * 1000; // `exp` is in seconds; convert to milliseconds
    } catch (error) {
        console.error("Token decoding failed", error);
        return true;
    }
};


const refreshToken = async (): Promise<string | null> => {
    try {
        const refreshToken = localStorage.getItem('refreshToken');
        const response = await axios.get('/api/v1/refresh', {
                        headers: {
                            Authorization: `Bearer ${refreshToken}`,
                        },
                    });
        const {data} = response.data.accessToken;
        localStorage.setItem('accessToken', data.accessToken);
        localStorage.setItem('refreshToken', data.refreshToken);
        return data;
    } catch (error) {
        console.error("Token refresh failed", error);
        return null;
    }
};


const ProtectedRoute: React.FC<ProtectedRouteProps> = ({children, requiredRole}) => {
    const [isAuthorized, setIsAuthorized] = useState<boolean | null>(null);

    useEffect(() => {
        const checkToken = async () => {
            let token = localStorage.getItem('accessToken');

            if (!token || isTokenExpired(token)) {
                token = await refreshToken();
                if (!token) {
                    localStorage.removeItem('accessToken');
                    localStorage.removeItem('refreshToken');
                    localStorage.removeItem('role');
                    setIsAuthorized(false);
                    return;
                }
            }

            const {role: decodedRole} = jwtDecode<TokenPayload>(token);
            if (
                (requiredRole === 'U' && (decodedRole === 'A' || decodedRole === 'U')) ||
                (requiredRole === 'A' && decodedRole === 'A')
            ) {
                setIsAuthorized(true);
            } else {
                setIsAuthorized(false);
            }
        };
        checkToken();
    }, [requiredRole]);

    if (isAuthorized === null) {
        return <CircularProgress />;
    }

    return isAuthorized ? children : <Navigate to={!isAuthorized ? "/unauthorized" : "/login"}/>;
};

export default ProtectedRoute;
