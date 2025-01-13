import React from 'react';
import { Box, Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import StyledTitle from '@/styles/StyledTitle';
import NavButton from '@/components/NavButton';

const Explanation: React.FC = () => {
  const navigate = useNavigate();

  return (
    <Box>
      <StyledTitle>Erklärung</StyledTitle>
      <Button
        variant="contained"
        color="primary"
        onClick={() => navigate('/blackbox')}
      >
        Erklärung
      </Button>
      <NavButton RouteTo="/results-gender">Weiter</NavButton>
    </Box>
  );
};

export default Explanation;
