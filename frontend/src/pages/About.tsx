import React from 'react';
import { Typography, Container, Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';

const About: React.FC = () => {
  const navigate = useNavigate();

  return (
    <Container>
      <h6>About HandScanAI</h6>
      <Typography variant="body1">
        Building a transparent, reliable, robust AI application to predict
        biometric information from hand images.
      </Typography>
      <Button
        variant="contained"
        color="primary"
        onClick={() => navigate('/information')}
        sx={{ marginTop: 2 }}
      >
        Information
      </Button>
      <Button
        variant="contained"
        color="primary"
        onClick={() => navigate('/berechnung')}
        sx={{ marginTop: 2 }}
      >
        Berechnung
      </Button>
    </Container>
  );
};

export default About;
