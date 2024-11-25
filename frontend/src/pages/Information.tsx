import React from 'react';
import { Typography, Container, Button, Box, styled } from '@mui/material';
import { useNavigate } from 'react-router-dom';
//import Stepper from '@/pages/Stepper';
import HorizStepper from '@/components/Stepper';
import BoxSx from '@/components/Box';
import { Title } from './Home';
import { Logo } from './Home';

const BoxText = styled(Typography)`
  font-family: 'Poppins', sans-serif;
  margin: 0 0 1.875rem;
  text-align: justify;
  font-size: clamp(1rem, 2vw, 1.5rem);
`;
const SecondaryHeading = styled(Typography)`
  font-family: 'Delius Unicase', cursive;
  margin: 0 0 1rem;
  text-align: left;
  font-size: clamp(1rem, 2vw, 1.5rem);
`;

const Information: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div>
      <div className="top">
        <Title variant="h2">Bevor wir Beginnen</Title>
        <img
          src="/HandLogo.png"
          alt="Logo von der Hand"
          style={{ maxWidth: '12%' }}
        />
      </div>

      <div className="information-container">
        <BoxSx>
          <SecondaryHeading>Daten statt Gebühren</SecondaryHeading>
          {/* <Title variant="h1">Daten statt Gebühren</Title> */}
          <BoxText>
            Wie bei vielen digitalen Diensten gilt auch hier: Statt eines
            klassischen Preises zahlen Sie mit etwas anderem – Ihren Daten. In
            unserer App sind es vor allem Ihre Interaktionen und die Bilder
            Ihrer Hand, die die KI verarbeitet und lernen lassen. Diese Daten
            sind der „Treibstoff“, der der KI hilft, intelligenter, präziser und
            anpassungsfähiger zu werden. Mit Ihren Eingaben tragen Sie aktiv
            dazu bei, dass das System weiterentwickelt und optimiert wird, um
            Ihnen und anderen Anwendern zukünftig noch bessere Ergebnisse zu
            bieten.
          </BoxText>
        </BoxSx>

        <BoxSx>
          <SecondaryHeading>Einwilligung zur Datennutzung</SecondaryHeading>
          <BoxText>
            Indem Sie unsere App nutzen, erklären Sie sich ausdrücklich damit
            einverstanden, dass Ihre Daten – einschließlich Ihrer Interaktionen
            und bereitgestellten Informationen – für die Verbesserung der
            KI-Modelle genutzt werden. Diese Daten werden dem Modell
            hinzugefügt. Unsere KI wird Open Source unter der MIT Lizenz von
            GitHub veröffentlicht. Das bedeutet, dass die Daten in einem
            öffentlich zugänglichen Modell weiterleben können. Ihre Daten
            bleiben dabei jedoch anonymisiert und werden nicht direkt einsehbar.
          </BoxText>
          <br></br>
          <p>
            Mit Ihrer Zustimmung stimmen Sie der Verarbeitung und
            Veröffentlichung Ihrer anonymisierten Daten innerhalb dieses
            Open-Source-Modells zu und tragen aktiv zur stetigen Verbesserung
            und Transparenz der KI bei. Weitere Informationen finden Sie hier:
            Datenschutzmerkblatt
          </p>
          <footer>
            <div className="checkbox">Ich akzeptiere die Datenverarbeitung</div>

            {/* Need to add Conditional Rendering here based on the checkbox */}
            <Button
              variant="contained"
              color="primary"
              onClick={() => navigate('/about')}
              sx={{ marginTop: 2 }}
            >
              Weiter
            </Button>
          </footer>
        </BoxSx>
      </div>
      <HorizStepper pageNumber={0}></HorizStepper>
    </div>
  );
};

export default Information;
