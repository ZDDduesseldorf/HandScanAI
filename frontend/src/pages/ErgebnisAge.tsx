import React from 'react';
import { Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import HorizStepper from '@/components/Stepper';
import TitleBar from '@/components/TitleBar';

const ErgebnisAge: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div>
      <TitleBar>Ergebnis</TitleBar>
      <Button
        variant="contained"
        color="primary"
        onClick={() => navigate('/ErgebnisGender')}
        disableElevation
        sx={{
          borderRadius: 0,
          backgroundColor: '#0F3EB5',
          fontFamily: 'Delius Unicase',
        }}
      >
        Weiter
      </Button>
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
    </div>
  );
};

export default ErgebnisAge;
