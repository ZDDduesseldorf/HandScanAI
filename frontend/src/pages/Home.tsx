import React from 'react';
import { Typography, Container, Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';

const Home: React.FC = () => {
  const navigate = useNavigate();

  return (
    <Container>
      <Typography variant="h2" component="h1" gutterBottom>
        Welcome to HandScanAI
      </Typography>
      <Typography variant="body1">
        This is the home page of HandScanAI
      </Typography>
      <Button
        variant="contained"
        color="primary"
        onClick={() => navigate('/about')}
        sx={{ marginTop: 2 }}
      >
        About
      </Button>
    </Container>
  );
};

export default Home;
