// FileUploadPopup.tsx

import React, {useState} from 'react';
import {
    Box,
    Button,
    CircularProgress,
    Dialog,
    DialogActions,
    DialogContent,
    DialogTitle,
    Typography
} from '@mui/material';
import {useDropzone} from 'react-dropzone';
import api from "../api/api.ts";

interface FileUploadPopupProps {
    open: boolean;
    onClose: () => void;
}

const FileUploadPopup: React.FC<FileUploadPopupProps> = ({open, onClose}) => {
    const [files, setFiles] = useState<File[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const onDrop = (acceptedFiles: File[]) => {
        setFiles(acceptedFiles);
        setError(null);
    };

    const handleUpload = async () => {
        if (!files) {
            setError('Please select file to upload.');
            return;
        }

        setLoading(true);
        const formData = new FormData();
        files.forEach(file => formData.append('files', file));

        try {
            await api.post('/files/upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            setLoading(false);
            onClose();
            window.location.reload();
        } catch (err) {
            setLoading(false);
            setError('Failed to upload files. Please try again.');
        }
    };

    const {getRootProps, getInputProps, isDragActive} = useDropzone({onDrop});

    return (
        <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
            <DialogTitle>Upload Files</DialogTitle>
            <DialogContent>
                <Box
                    {...getRootProps()}
                    sx={{
                        border: '2px dashed',
                        borderColor: 'primary.main',
                        padding: '20px',
                        textAlign: 'center',
                        cursor: 'pointer',
                        borderRadius: '8px',
                        backgroundColor: isDragActive ? 'primary.light' : 'background.paper',
                    }}
                >
                    <input {...getInputProps()} />
                    {isDragActive ? (
                        <Typography variant="body1" color="textSecondary">
                            Drop the file here...
                        </Typography>
                    ) : (
                        <Typography variant="body1" color="textSecondary">
                            Drag & drop file here, or click to select file
                        </Typography>
                    )}
                </Box>

                {files.length > 0 && (
                    <Box mt={2}>
                        <ul>
                            {files.map(file => (
                                <li key={file.name}>
                                    <Typography variant="body2" color="textSecondary">
                                        {file.name} - {file.size} bytes
                                    </Typography>
                                </li>
                            ))}
                        </ul>
                    </Box>
                )}

                {error && (
                    <Typography color="error" variant="body2" mt={2}>
                        {error}
                    </Typography>
                )}
            </DialogContent>

            <DialogActions>
                <Button onClick={onClose} color="secondary">
                    Cancel
                </Button>
                <Button onClick={handleUpload} color="primary" disabled={loading}>
                    {loading ? <CircularProgress size={24}/> : 'Upload'}
                </Button>
            </DialogActions>
        </Dialog>
    );
};

export default FileUploadPopup;
