import React from 'react';
import { Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import HorizStepper from '@/components/Stepper';
import TitleBar from '@/components/TitleBar';
import NavButton from '@/components/NavButton';
import { BodyLayout } from './Information';

const ErgebnisAge: React.FC = () => {
  const navigate = useNavigate();

  return (
    <BodyLayout>
      <TitleBar>Ergebnis</TitleBar>
      <NavButton RouteTo="/ErgebnisGender">Weiter</NavButton>
      <br></br>
      <br></br>

      <Button
        variant="contained"
        color="primary"
        onClick={() => navigate('/BlackBox')}
        disableElevation
        sx={{
          borderRadius: 0,
          backgroundColor: '#0F3EB5',
          fontFamily: 'Delius Unicase',
        }}
      >
        Erklärung
      </Button>
      <HorizStepper pageNumber={3}></HorizStepper>
    </BodyLayout>
  );
};

export default ErgebnisAge;
