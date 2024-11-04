import React from 'react';
import { Typography, Container } from '@mui/material';

const About: React.FC = () => {
  return (
    <Container>
      <Typography variant="h2" component="h1" gutterBottom>
        About HandScanAI
      </Typography>
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
    </Container>
  );
};

export default About;
