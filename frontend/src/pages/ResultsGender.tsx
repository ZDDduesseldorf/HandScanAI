import React from 'react';
import StyledTitle from '@/styles/StyledTitle';
import NavButton from '@/components/NavButton';
import { Box } from '@mui/material';

const ResultsGender: React.FC = () => {
  return (
    <Box>
      <StyledTitle>Ergebnis</StyledTitle>
      <NavButton RouteTo="/submission-complete">Weiter</NavButton>
    </Box>
  );
};

export default ResultsGender;
