import React from 'react';
import { Typography, Container, Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';
//import Stepper from '@/pages/Stepper';
import HorizontalLinearAlternativeLabelStepper from '@/components/Stepper';

const Information: React.FC = () => {
  const navigate = useNavigate();

  return (
    <Container>
      <Typography variant="h1" component="h1" gutterBottom>
        Informationen
      </Typography>
      <Button
        variant="contained"
        color="primary"
        onClick={() => navigate('/about')}
        sx={{ marginTop: 2 }}
      >
        Weiter
      </Button>

      <HorizontalLinearAlternativeLabelStepper></HorizontalLinearAlternativeLabelStepper>
    </Container>
  );
};

export default Information;
