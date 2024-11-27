import React from 'react';
import { Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import HorizStepper from '@/components/Stepper';

const ErgebnisGender: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div>
      <div>Danke</div>
      <Button
        variant="contained"
        color="primary"
        onClick={() => navigate('/Home')}
        // sx={{ marginTop: 2 }}
      >
        Beenden
      </Button>
      <HorizStepper pageNumber={3}></HorizStepper>
    </div>
  );
};

export default ErgebnisGender;
