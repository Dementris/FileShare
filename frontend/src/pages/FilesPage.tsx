import React, {useEffect, useState} from 'react';
import {
    Box,
    Button,
    Card,
    CardActions,
    CardContent,
    CircularProgress,
    Grid,
    IconButton,
    Typography,
} from '@mui/material';
import ImageIcon from '@mui/icons-material/Image';
import PictureAsPdfIcon from '@mui/icons-material/PictureAsPdf';
import VideoLibraryIcon from '@mui/icons-material/VideoLibrary';
import InsertDriveFileIcon from '@mui/icons-material/InsertDriveFile';
import api from "../api/api.ts";
import UserPermissionPopup from "../components/UserPermissionPopUp.tsx";
import DeleteIcon from '@mui/icons-material/Delete';
import {useNavigate} from "react-router-dom";

interface File {
    id: number;
    name: string;
    type: string;
    size: number;
    created_at: string;
    updated_at: string;
    owner: {
        id: number;
        username: string;
        email: string;
        role: string;
    };
    permission: 'view' | 'download';
}

// Function to get the appropriate icon based on file type
const getFileIcon = (type: string) => {
    switch (type) {
        case 'jpg':
        case 'jpeg':
        case 'png':
        case 'gif':
            return <ImageIcon fontSize="large"/>;
        case 'pdf':
            return <PictureAsPdfIcon fontSize="large"/>;
        case 'mp4':
        case 'avi':
        case 'mov':
            return <VideoLibraryIcon fontSize="large"/>;
        default:
            return <InsertDriveFileIcon fontSize="large"/>;
    }
};

const FileDashboard: React.FC = () => {
    const [files, setFiles] = useState<File[]>([]);
    const [loading, setLoading] = useState(true);
    const [openPopup, setOpenPopup] = useState(false);
    const [selectedFileId, setSelectedFileId] = useState<number | null>(null);
    const navigate = useNavigate();

    const handleOpenPopup = (fileId: number) => {
        setSelectedFileId(fileId);
        setOpenPopup(true)
    };
    const handleClosePopup = () => setOpenPopup(false);
    const role = localStorage.getItem("role")

    useEffect(() => {
        const fetchFiles = async () => {
            try {
                const response = await api.get('/files');
                // Ensure the data is an array before setting it to files
                if (Array.isArray(response.data)) {
                    setFiles(response.data);
                } else {
                    console.error('Unexpected response data:', response.data);
                }
            } catch (error) {
                console.error('Failed to fetch files:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchFiles();
    }, []);

    const handleDownload = async (fileId: number) => {
        try {
            const response = await api.get(`/files/download/${fileId}`);
            if (response.status === 200) {
                const link = document.createElement('a');
                link.href = response.data.downloadUrl;
                link.setAttribute('download', "");
                document.body.appendChild(link);
                link.click();

                // Clean up
                link.remove();
            } else {
                console.error('File download failed:', response.status);
            }
        } catch (error) {
            console.error('Error downloading file:', error);
        }
    };

    const handleDelete = async (fileId: number) => {
        try {
            const response = await api.delete(`files/${fileId}`)
            if (response.status === 204){
                navigate("/files")
            }
        }catch (error){
            console.error('Error deleting file:', error);
        }
    }

    if (loading) {
        return (
            <Box display="flex" justifyContent="center" alignItems="center" height="100vh">
                <CircularProgress/>
            </Box>
        );
    }


    return (
        <Box padding={4}>
            <Typography variant="h4" gutterBottom>
                File Dashboard
            </Typography>
            <Grid container spacing={3}>
                {files.map((file) => (
                    <Grid item xs={12} sm={6} md={4} key={file.id}>
                        <Card>
                            <CardActions style={{justifyContent: 'flex-end'}}>
                                {role === 'admin' && (
                                    <IconButton size="small"
                                                onClick={() => handleDelete(file.id)}
                                                sx={{
                                        color: '#f44336', // Red color
                                        backgroundColor: 'rgba(244, 67, 54, 0.1)',
                                        '&:hover': {
                                            backgroundColor: 'rgba(244, 67, 54, 0.2)',
                                        },
                                    }}>
                                        <DeleteIcon fontSize="medium"/>
                                    </IconButton>)}
                            </CardActions>
                            <CardContent>
                                {/* Display file icon based on type */}
                                <Box display="flex" justifyContent="center" alignItems="center" mb={2}>
                                    {getFileIcon(file.type)}
                                </Box>
                                <Typography variant="h6" component="div" align="center">
                                    {file.name}
                                </Typography>
                                <Typography color="textSecondary" align="center">
                                    Type: {file.type.toUpperCase()}
                                </Typography>
                                <Typography color="textSecondary" align="center">
                                    Size: {(file.size / (1024 * 1024)).toFixed(2)} MB
                                </Typography>
                                <Typography color="textSecondary" align="center">
                                    Created At: {new Date(file.created_at).toLocaleDateString()}
                                </Typography>
                                <Typography color="textSecondary" align="center">
                                    Owner: {file.owner.username} ({file.owner.role})
                                </Typography>
                            </CardContent>
                            <CardActions style={{justifyContent: 'center'}}>
                                {file.permission === 'download' && (
                                    <Button
                                        size="small"
                                        color="primary"
                                        variant="contained"
                                        onClick={() => handleDownload(file.id)}
                                    >
                                        Download
                                    </Button>
                                )}
                                {role === 'admin' && (
                                    <Box>
                                        <Button variant="outlined" onClick={() => handleOpenPopup(file.id)}>
                                            Manage Permissions
                                        </Button>
                                        <UserPermissionPopup open={openPopup} onClose={handleClosePopup}
                                                             fileId={selectedFileId}/>
                                    </Box>
                                )
                                }
                            </CardActions>
                        </Card>
                    </Grid>
                ))}
            </Grid>
        </Box>
    );
};

export default FileDashboard;
