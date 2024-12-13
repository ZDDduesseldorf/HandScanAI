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
        // sx={{ marginTop: 2 }}
      >
        Weiter
      </Button>
      <HorizStepper pageNumber={3}></HorizStepper>
    </div>
  );
};

export default ErgebnisAge;
