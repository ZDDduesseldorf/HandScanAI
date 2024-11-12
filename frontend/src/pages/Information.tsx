import React from 'react';
import { Typography, Container, Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';
//import Stepper from '@/pages/Stepper';
import HorizontalLinearAlternativeLabelStepper from '@/components/Stepper';
import BoxSx from '@/components/Box';

const Information: React.FC = () => {
  const navigate = useNavigate();

  return (
    <Container>
      <Typography variant="h2" component="h2" gutterBottom>
        Informationen
      </Typography>
      <BoxSx>
        <h3 style={{ margin: 0 }}>Einverständnis für Dateneingabe</h3>
        <p>
          Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam
          nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat,
          sed diam voluptua. At vero eos et accusam et justo duo dolores et ea
          rebum. Stet clita kasd gubergren, no sea takimata sanctus est
        </p>

        <Button
          variant="contained"
          color="primary"
          onClick={() => navigate('/about')}
          sx={{ marginTop: 2 }}
        >
          Weiter
        </Button>
      </BoxSx>

      <HorizontalLinearAlternativeLabelStepper></HorizontalLinearAlternativeLabelStepper>
    </Container>
  );
};

export default Information;
