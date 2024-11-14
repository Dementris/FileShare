import React, {useState, useEffect} from 'react';
import {
    Dialog,
    DialogTitle,
    DialogContent,
    TextField,
    List,
    ListItem,
    ListItemText,
    Button,
    Grid, Checkbox,
} from '@mui/material';
import api from "../api/api.ts";

interface User {
    id: number;
    email: string;
}

interface PopupProps {
    open: boolean;
    onClose: () => void;
    file_id: number;
}

const UserPermissionPopup: React.FC<PopupProps> = ({open, onClose}) => {
    const [users, setUsers] = useState<User[]>([]);
    const [searchUser, setSearchUser] = useState('');
    const [searchPermission, setSearchPermission] = useState('');
    const [selectedUsers, setSelectedUsers] = useState<number[]>([]);

    const fetchUsers = async () => {
        try {
            const response = await api.get('/users');
            setUsers(response.data);
        } catch (error) {
            console.error("Error fetching users:", error);
        }
    };
    useEffect(() => {
        if (open) {
            fetchUsers();
        }
    }, [open]);

    const handleToggleUser = (userId: number) => {
        setSelectedUsers((prev) =>
            prev.includes(userId) ? prev.filter((id) => id !== userId) : [...prev, userId]
        );
    };

    return (
        <Dialog open={open} onClose={onClose} fullWidth maxWidth="sm">
            <DialogTitle>Manage Users and Permissions</DialogTitle>
            <DialogContent>
                <Grid container spacing={2}>
                    <Grid item xs={6}>
                        <TextField
                            label="Search Users"
                            fullWidth
                            variant="outlined"
                            value={searchUser}
                            onChange={(e) => setSearchUser(e.target.value)}
                        />
                        <List sx={{
                            maxHeight: 300,
                            overflowY: 'auto',
                            border: '1px solid #ddd',
                            borderRadius: '4px',
                            mt: 1,
                        }}>
                            {users.map((user) => (
                                <ListItem key={user.id} disablePadding sx={{
                                    color: 'text.primary',
                                    typography: 'body1',
                                    boxShadow: '0 8px 16px rgba(255, 0, 255, 0.5)',
                                    padding: '10px',
                                    borderRadius: '4px',
                                    transform: 'scale(1.05)',
                                }}>
                                    <Checkbox
                                        checked={selectedUsers.includes(user.id)}
                                        onChange={() => handleToggleUser(user.id)}
                                    />
                                    <ListItemText primary={user.email} color={"white"}/>
                                </ListItem>
                            ))}
                        </List>
                    </Grid>
                    <Grid item xs={6}>
                        <TextField
                            label="Search Permissions"
                            fullWidth
                            variant="outlined"
                            value={searchPermission}
                            onChange={(e) => setSearchPermission(e.target.value)}
                        />
                        <List>
                            {users.map((permission) => (
                                <ListItem key={permission.id} sx={{
                                    color: 'text.primary',
                                    typography: 'body2',
                                    boxShadow: '0 8px 16px rgba(255, 0, 255, 0.5)',
                                    padding: '10px',
                                    borderRadius: '4px',
                                    transform: 'scale(1.05)',
                                }}>
                                    <ListItemText primary={permission.email}/>
                                </ListItem>
                            ))}
                        </List>
                    </Grid>
                </Grid>
                <Button
                    variant="contained"
                    color="primary"
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
