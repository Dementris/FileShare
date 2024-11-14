// src/components/ProtectedRoute.tsx
import React from 'react';
import {Navigate} from 'react-router-dom';
import {jwtDecode} from 'jwt-decode';

interface ProtectedRouteProps {
    children: JSX.Element;
    requiredRole: 'U' | 'A';
}

interface TokenPayload {
    exp: number;
    role: 'U' | 'A';
}

const isTokenExpired = (token: string): boolean => {
    try {
        const {exp} = jwtDecode<TokenPayload>(token);
        return Date.now() >= exp * 1000; // exp is in seconds; convert to milliseconds
    } catch (error) {
        console.error("Token decoding failed", error);
        return true;
    }
};

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({children, requiredRole}) => {
    const token = localStorage.getItem('accessToken');

    if (!token || isTokenExpired(token)) {
        localStorage.removeItem('accessToken'); // Clear any expired tokens
        localStorage.removeItem('role');
        return <Navigate to="/login"/>;
    }

    const {role: decodedRole} = jwtDecode<TokenPayload>(token);
    if (
        (requiredRole === 'U' && (decodedRole === 'A' || decodedRole === 'U')) ||
        (requiredRole === 'A' && decodedRole === 'A')
    ) {
        return children;
    }
    return <Navigate to="/unauthorized"/>;
};

export default ProtectedRoute;
