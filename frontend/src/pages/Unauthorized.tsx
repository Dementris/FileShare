import {Container, Typography} from "@mui/material";

const Unauthorized: React.FC = () => {
    return (
        <Container maxWidth="sm">
            <Typography variant="h4" component="h1">403 - Unauthorized</Typography>
            <Typography>You do not have permission to view this page.</Typography>
        </Container>
    );
};

export default Unauthorized;