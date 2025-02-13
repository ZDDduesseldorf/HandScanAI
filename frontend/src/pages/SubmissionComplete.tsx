import React from 'react';
import { Box, Typography, styled } from '@mui/material';
import StyledTitle from '@/styles/StyledTitle';
import NavButton from '@/components/buttons/Navigation';

const SecondaryHeading = styled(Typography)`
  display: flex;
  font-family: 'Delius Unicase', cursive;
  margin: 0 0 2rem;
  left-padding: 2rem;
  text-align: left;
  font-size: clamp(1rem, 2vw, 1.5rem);
  color: #1a3ab8;
`;
const BoxText = styled(Typography)`
  font-family: 'Poppins', sans-serif;
  margin: 0 0 1 rem;
  text-align: justify;
  font-size: clamp(1rem, 2vw, 1.5rem);
  color: #1a3ab8;
`;

const SubmissionComplete: React.FC = () => {
  return (
    <Box>
      <StyledTitle>Danke</StyledTitle>
      <SecondaryHeading>Wir hoffen du hattest Spaß</SecondaryHeading>
      <BoxText>
        Über den untenstehenden QR kannst du dir deine Ergebnisse der
        Handanalyse und weiteres Wissen zum Thema KI downloaden. HandScan AI hat
        einen eigenen Bericht für dich erstellt. Vielen Dank, dass du mit deiner
        Nutzung geholfen hast, HandScan AI zu verbessern. Bis bald!
      </BoxText>
      <NavButton RouteTo="/">Beenden</NavButton>
    </Box>
  );
};

export default SubmissionComplete;
