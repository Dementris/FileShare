import React, {useEffect, useState} from 'react';
import {
    Button,
    Checkbox,
    Dialog,
    DialogContent,
    DialogTitle,
    Grid,
    IconButton,
    List,
    ListItem,
    ListItemText,
    Typography,
} from '@mui/material';
import api from "../api/api.ts";
import DeleteIcon from "@mui/icons-material/Delete";

interface User {
    id: number;
    email: string;
}

interface PopupProps {
    open: boolean;
    onClose: () => void;
    fileId: number | null
}

const UserPermissionPopup: React.FC<PopupProps> = ({open, onClose, fileId}) => {
    const [users, setUsers] = useState<User[]>([]);
    const [notUsers, setNotUsers] = useState<User[]>([])
    const [selectedUsers, setSelectedUsers] = useState<number[]>([]);

    const fetchUsers = async () => {
        try {
            const response = await api.get(`/users/permission/${fileId}`);
            setUsers(response.data);
        } catch (error) {
            console.error("Error fetching users:", error);
        }
    };
    const fetchNotUsers = async () => {
        try {
            const response = await api.get(`/users/permission/not/${fileId}`);
            setNotUsers(response.data);
        } catch (error) {
            console.error("Error fetching users:", error);
        }
    };

    useEffect(() => {
        if (open) {
            fetchUsers();
            fetchNotUsers()
        }
    }, [open]);

    const handleToggleUser = (userId: number) => {
        setSelectedUsers((prev) =>
            prev.includes(userId) ? prev.filter((id) => id !== userId) : [...prev, userId]
        );
    };

    const handleDeletePermission = async (userId: number) => {
        const response = await api.delete(`/files/permissions/${fileId}/${userId}`);
        await fetchUsers();
        await fetchNotUsers()
        if (response.status == 403){
            console.error("Error deleting permission")
        }
    }
    const handleUpdate = async () => {
        try {
        const promises = selectedUsers.map(userId =>
            api.post(`/files/permissions/${fileId}/${userId}`)
        );

        const responses = await Promise.all(promises);
        console.log("All permissions updated successfully:", responses);
        setSelectedUsers([]);
        await fetchUsers();
        await fetchNotUsers()
        } catch (error) {
        console.error("Error updating permissions for some users:", error);
    }
    }



    return (
        <Dialog open={open} onClose={onClose} fullWidth maxWidth="sm">
            <DialogTitle>Manage Users and Permissions {fileId}</DialogTitle>
            <DialogContent>
                <Grid container spacing={2}>
                    {/* Left Column: Not yet users with permission */}
                    <Grid item xs={6}>
                        <Typography variant="body1" sx={{mb: 2}}>Users</Typography>
                        {notUsers && (
                            <List sx={{
                                maxHeight: 300,
                                overflowY: 'auto',
                                border: '1px solid #ddd',
                                borderRadius: '4px',
                                mt: 1,
                            }}>
                                {notUsers.map((notUser) => (
                                    <ListItem key={notUser.id} disablePadding sx={{
                                        color: 'text.primary',
                                        typography: 'body1',
                                        boxShadow: '0 8px 16px rgba(255, 0, 255, 0.5)',
                                        padding: '10px',
                                        borderRadius: '4px',
                                        transform: 'scale(1.05)',
                                    }}>
                                        <Checkbox
                                            checked={selectedUsers.includes(notUser.id)}
                                            onChange={() => handleToggleUser(notUser.id)}
                                        />
                                        <ListItemText primary={notUser.email} color={"white"}/>
                                    </ListItem>
                                ))}
                            </List>
                        )}
                    </Grid>

                    {/* Right Column: Users with permission and Remove button */}
                    <Grid item xs={6}>
                        <Typography variant="body1" sx={{mb: 2}}>Users with Permission</Typography>
                        {users && (
                            <List sx={{
                                maxHeight: 300,
                                overflowY: 'auto',
                                border: '1px solid #ddd',
                                borderRadius: '4px',
                                mt: 1,
                            }}>
                                {users.map((user) => (
                                    <ListItem key={user.id}>
                                        <ListItemText primary={user.email}/>
                                        {/* Remove Permission Button */}
                                        <IconButton size="small"
                                                    onClick={() => handleDeletePermission(user.id)}
                                                    sx={{
                                                        color: '#f44336', // Red color
                                                        backgroundColor: 'rgba(244, 67, 54, 0.1)',
                                                        '&:hover': {
                                                            backgroundColor: 'rgba(244, 67, 54, 0.2)',
                                                        },
                                                    }}>
                                            <DeleteIcon fontSize="medium"/>
                                        </IconButton>
                                    </ListItem>
                                ))}
                            </List>
                        )}
                    </Grid>
                </Grid>

                {/* Submit Button */}
                <Button
                    variant="contained"
                    color="primary"
                    onClick={() => handleUpdate()}
                    disabled={selectedUsers.length === 0}
                    sx={{mt: 2}}
                >
                    Submit
                </Button>
            </DialogContent>
        </Dialog>
    );
};

export default UserPermissionPopup;
