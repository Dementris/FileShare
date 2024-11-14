// src/App.tsx
import {BrowserRouter as Router, Routes, Route, useLocation} from 'react-router-dom';
import Login from './pages/Login';
import AdminPage from './pages/AdminPage.tsx';
import ProtectedRoute from './components/ProtectedRoute';
import Main from "./pages/Main.tsx";
import Signup from "./pages/Signup.tsx";
import Navbar from "./components/Navbar.tsx";
import FilesPage from "./pages/FilesPage.tsx";

const App = () => {
    return (
        <Router>
            <MainLayout />
        </Router>
    );
};

const MainLayout = () => {
    const location = useLocation();
    const hideNavbarPaths = ['/', '/login', '/signup'];
    const shouldShowNavbar = !hideNavbarPaths.includes(location.pathname);

    return (
        <>
            {shouldShowNavbar && <Navbar />}
            <Routes>
                <Route path="/" element={<Main />} />
                <Route path="/login" element={<Login />} />
                <Route path="/signup" element={<Signup />} />

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
