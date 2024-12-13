import React from 'react';
import { Button, Typography, styled } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import HorizStepper from '@/components/Stepper';
import TitleBar from '@/components/TitleBar';
// import { FontText } from './Berechnung';

const SecondaryHeading = styled(Typography)`
  display: flex;
  font-family: 'Delius Unicase', cursive;
  margin: 0 0 2rem;
  left-padding: 2rem;
  text-align: left;
  font-size: clamp(1rem, 2vw, 1.5rem);
`;
const BoxText = styled(Typography)`
  font-family: 'Poppins', sans-serif;
  margin: 0 0 1 rem;
  text-align: justify;
  font-size: clamp(1rem, 2vw, 1.5rem);
  // font-size: 0.8rem;
`;

const ErgebnisGender: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div>
      <TitleBar>Danke</TitleBar>
      <div style={{ padding: '2rem' }}>
        <SecondaryHeading>Wir hoffen du hattest Spaß</SecondaryHeading>
        <BoxText>
          Über den untenstehenden QR kannst du dir deine Ergebnisse der
          Handanalyse und weiteres Wissen zum Thema KI downloaden. HandScan AI
          hat einen eigenen Beericht für dich erstellt. Vielen Dank, dass du mit
          deiner Nutzung geholfen hast, HandScan AI zu verbessern. Bis bald!
        </BoxText>

        <Button
          variant="contained"
          color="primary"
          onClick={() => navigate('/Home')}
          disableElevation
          sx={{
            borderRadius: 0,
            backgroundColor: '#0F3EB5',
            width: '20em',
            height: '3.5em',
            fontFamily: 'Delius Unicase',
          }}
          // sx={{ marginTop: 2 }}
        >
          Beenden
        </Button>
      </div>

      <HorizStepper pageNumber={3}></HorizStepper>
    </div>
  );
};

export default ErgebnisGender;
