import React from 'react';
import { Button, Typography, styled } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import HorizStepper from '@/components/Stepper';
import { Title } from './Home';
import { BodyLayout, HorizontalBar } from './Information';
import NavButton from '@/components/NavButton';

export const FontText = styled(Typography)`
  font-family: 'Delius Unicase', cursive;
  color: #1a3ab8;
  margin: 0 0 1 rem;
  text-align: center;
  // font-size: clamp(1rem, 2vw, 1.5rem);
  display: flex;
  justify-content: center; // Horizontale Zentrierung
  align-items: center; // Vertikale Zentrierung
  position: absolute; // Ermöglicht es, das Element mit 'top', 'left' etc. zu positionieren
  top: 50%; // Vertikal in der Mitte
  left: 50%; // Horizontal in der Mitte
  transform: translate(-50%, -50%);
`;

const Berechnung: React.FC = () => {
  const navigate = useNavigate();

  return (
    <BodyLayout>
      <HorizontalBar>
        <Title variant="h1">Berechnung</Title>

        <img
          src="/HandLogo.png"
          alt="Logo von der Hand"
          //style={{ maxWidth: '30%', marginTop: '10px' }}
        />
      </HorizontalBar>

      <FontText>
        Ungefähr 90% der Menschen sind Rechtshänder,<br></br>
        wobei die Handdominanz oft in der frühen Kindheit <br></br>
        festgelegt wird und teilweise genetisch beeinflusst<br></br> ist.
      </FontText>
      <NavButton RouteTo="/ErgebnisAge">Weiter</NavButton>

      <Button
        variant="contained"
        color="primary"
        onClick={() => navigate('/Bildaufnahme')}
        sx={{
          borderRadius: 0,
          backgroundColor: '#0F3EB5',
          fontFamily: 'Delius Unicase',
        }}
      >
        Bildaufnahme
      </Button>

      <HorizStepper pageNumber={2}></HorizStepper>
    </BodyLayout>
  );
};

export default Berechnung;
