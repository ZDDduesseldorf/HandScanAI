import React from 'react';
import { Typography, Button, Box, styled } from '@mui/material';
import { useNavigate } from 'react-router-dom';
//import Stepper from '@/pages/Stepper';
import HorizStepper from '@/components/Stepper';
import BoxSx from '@/components/Box';
import TitleBar from '@/components/TitleBar';
import NavButton from '@/components/NavButton';

export const BodyLayout = styled(Box)`
  margin: 20px;
  margin-right: 30px;
  margin-left: 30px;
`;

export const HorizontalBar = styled(Box)`
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  min-width: 100%;
  align-items: center;
`;
const BoxLayout = styled(Box)`
  display: flex;
  flex-direction: column;
  justify-content: space-between;

  gap: 20px; /* Optional: adds space between the two boxes */
}
`;
const BoxText = styled(Typography)`
  font-family: 'Poppins', sans-serif;
  margin: 0 0 1 rem;
  text-align: justify;
  // font-size: clamp(1rem, 2vw, 1.5rem);
  font-size: 0.8rem;
`;
const SecondaryHeading = styled(Typography)`
  font-family: 'Delius Unicase', cursive;
  margin: 0 0 0.5rem;
  text-align: left;
  font-size: clamp(1rem, 2vw, 1.5rem);
`;

const Information: React.FC = () => {
  const navigate = useNavigate();

  return (
    <BodyLayout>
      <TitleBar>Bevor wir Beginnen</TitleBar>
      <BoxLayout>
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

          <BoxText>
            <br></br>
            Mit Ihrer Zustimmung stimmen Sie der Verarbeitung und
            Veröffentlichung Ihrer anonymisierten Daten innerhalb dieses
            Open-Source-Modells zu und tragen aktiv zur stetigen Verbesserung
            und Transparenz der KI bei. Weitere Informationen finden Sie hier:
            Datenschutzmerkblatt
          </BoxText>
          <HorizontalBar>
            <BoxText className="checkbox">
              Ich akzeptiere die Datenverarbeitung
            </BoxText>
            <NavButton RouteTo="/Berechnung">Weiter</NavButton>
          </HorizontalBar>
        </BoxSx>
      </BoxLayout>
      <br></br>
      <HorizStepper pageNumber={0}></HorizStepper>
    </BodyLayout>
  );
};

export default Information;
