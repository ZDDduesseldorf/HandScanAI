import React from 'react';
import { Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import StyledTitle from '@/styles/StyledTitle';

const ResultsAge: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div>
      <StyledTitle>Ergebnis</StyledTitle>
      <Button
        variant="contained"
        color="primary"
        onClick={() => navigate('/blackbox')}
      >
        Erklärung
      </Button>
      <Button
        variant="contained"
        color="primary"
        onClick={() => navigate('/results-gender')}
      >
        Weiter
      </Button>
    </div>
  );
};

export default ResultsAge;
