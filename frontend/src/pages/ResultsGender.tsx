import React from 'react';
import { Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import StyledTitle from '@/styles/StyledTitle';

const ResultsGender: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div>
      <StyledTitle>Ergebnis</StyledTitle>
      <Button
        variant="contained"
        color="primary"
        onClick={() => navigate('/submission-complete')}
      >
        Weiter
      </Button>
    </div>
  );
};

export default ResultsGender;
