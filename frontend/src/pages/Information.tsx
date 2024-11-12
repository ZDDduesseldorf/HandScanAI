import React from 'react';
import { Typography, Container, Button, Box } from '@mui/material';
import { useNavigate } from 'react-router-dom';
//import Stepper from '@/pages/Stepper';
import HorizontalLinearAlternativeLabelStepper from '@/components/Stepper';
import BoxSx from '@/components/Box';

import './Information.css';

const Information: React.FC = () => {
  const navigate = useNavigate();

  return (
    <Container>
      <Typography variant="h3" component="h3" gutterBottom>
        Informationen
      </Typography>
      <div className="information-container">
        <BoxSx>
          <h3 style={{ margin: 0 }}>Einverständnis für Dateneingabe</h3>
          <p>
            Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam
            nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam
            erat, sed diam voluptua. At vero eos et accusam et justo duo dolores
            et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est
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

        <BoxSx>
          <h3>Richtige Handstellung</h3>
          <img
            src="/Hand1.png"
            alt="Handstellung"
            style={{ maxWidth: '40%', marginTop: '10px' }}
          />
          <img
            src="/Hand2.png"
            alt="Handstellung"
            style={{ maxWidth: '40%', marginTop: '10px' }}
          />
          <img
            src="/Hand3.png"
            alt="Handstellung"
            style={{ maxWidth: '40%', marginTop: '10px' }}
          />
        </BoxSx>
      </div>
      <HorizontalLinearAlternativeLabelStepper></HorizontalLinearAlternativeLabelStepper>
    </Container>
  );
};

export default Information;
