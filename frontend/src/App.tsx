// src/App.tsx
import {BrowserRouter as Router, Routes, Route, useLocation} from 'react-router-dom';
import Login from './pages/Login';
import AdminPage from './pages/AdminPage.tsx';
import ProtectedRoute from './components/ProtectedRoute';
import Main from "./pages/Main.tsx";
import Signup from "./pages/Signup.tsx";
import Navbar from "./components/Navbar.tsx";
import FilesPage from "./pages/FilesPage.tsx";
import RegistrationSuccessPage from "./pages/RegistrationSuccessPage.tsx";
import Unauthorized from "./pages/Unauthorized.tsx";

const App = () => {
    console.log(import.meta.env.VITE_APP_TITLE)
    console.log(import.meta.env.VITE_BACKEND_URL)
    console.log(import.meta.env.VITE_REFRESH_TOKEN_URL)
    return (
        <Router>
            <MainLayout />
        </Router>
    );
};

const MainLayout = () => {
    const location = useLocation();
    const hideNavbarPaths = ['/', '/login', '/signup', '/registration-success'];
    const shouldShowNavbar = !hideNavbarPaths.includes(location.pathname);

    return (
        <>
            {shouldShowNavbar && <Navbar />}
            <Routes>
                <Route path="/" element={<Main />} />
                <Route path="/login" element={<Login />} />

                <Route path="/signup" element={<Signup />} />
                <Route path="/registration-success" element={<RegistrationSuccessPage />} />

                <Route path="/unauthorized" element={<Unauthorized />} />
                {/* Protected Routes */}
                <Route
                    path="/files"
                    element={
                        <ProtectedRoute requiredRole="U">
                            <FilesPage />
                        </ProtectedRoute>
                    }
                />
                <Route
                    path="/admin"
                    element={
                        <ProtectedRoute requiredRole="A">
                            <AdminPage />
                        </ProtectedRoute>
                    }
                />
            </Routes>
        </>
    );
};

export default App;
