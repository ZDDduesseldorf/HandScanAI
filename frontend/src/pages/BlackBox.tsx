import React from 'react';
import { Typography, Box, styled } from '@mui/material';
//import Stepper from '@/pages/Stepper';
import HorizStepper from '@/components/Stepper';

import { BodyLayout } from './Information';
import TitleBar from '@/components/TitleBar';
import NavButton from '@/components/NavButton';

// this is just the Layout
const BottomMiddleLayout = styled(Box)`
  display: flex;
  flex-direction: row;
  justify-content: space-between;

  gap: 20px; /* Optional: adds space between the two boxes */
}
`;
const UpperMiddleLayout = styled(Box)`
  display: flex;
  flex-direction: column;
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

const BlackBox: React.FC = () => {
  return (
    <BodyLayout>
      <TitleBar>Black-Box KI</TitleBar>
      <UpperMiddleLayout>
        <SecondaryHeading>K-nearest neighbor modell</SecondaryHeading>
        {/* <Title variant="h1">Daten statt Gebühren</Title> */}
        <BoxText>
          Wie bei vielen digitalen Diensten gilt auch hier: Statt eines
          klassischen Preises zahlen Sie mit etwas anderem – Ihren Daten. In
          unserer App sind es vor allem Ihre Interaktionen und die Bilder Ihrer
          Hand, die die KI verarbeitet und lernen lassen. Diese Daten sind der
          „Treibstoff“, der der KI hilft, intelligenter, präziser und
          anpassungsfähiger zu werden. Mit Ihren Eingaben tragen Sie aktiv dazu
          bei, dass das System weiterentwickelt und optimiert wird, um Ihnen und
          anderen Anwendern zukünftig noch bessere Ergebnisse zu bieten.
        </BoxText>
        <BottomMiddleLayout>
          <div>
            <SecondaryHeading style={{ fontSize: '1rem' }}>
              Trainingsdaten
            </SecondaryHeading>
            <BoxText>
              Indem Sie unsere App nutzen, erklären Sie sich ausdrücklich damit
              einverstanden, dass Ihre Daten – einschließlich Ihrer
              Interaktionen und bereitgestellten Informationen – für die
              Verbesserung der KI-Modelle genutzt werden. Diese Daten werden dem
              Modell hinzugefügt. Unsere KI wird Open Source unter der MIT
              Lizenz von GitHub veröffentlicht. Das bedeutet, dass die Daten in
              einem öffentlich zugänglichen Modell weiterleben können. Ihre
              Daten bleiben dabei jedoch anonymisiert und werden nicht direkt
              einsehbar.
            </BoxText>
          </div>

          <div>
            <SecondaryHeading style={{ fontSize: '1rem' }}>
              Embeddings
            </SecondaryHeading>
            <BoxText>
              Indem Sie unsere App nutzen, erklären Sie sich ausdrücklich damit
              einverstanden, dass Ihre Daten – einschließlich Ihrer
              Interaktionen und bereitgestellten Informationen – für die
              Verbesserung der KI-Modelle genutzt werden. Diese Daten werden dem
              Modell hinzugefügt. Unsere KI wird Open Source unter der MIT
              Lizenz von GitHub veröffentlicht. Das bedeutet, dass die Daten in
              einem öffentlich zugänglichen Modell weiterleben können. Ihre
              Daten bleiben dabei jedoch anonymisiert und werden nicht direkt
              einsehbar.
            </BoxText>
          </div>
        </BottomMiddleLayout>
      </UpperMiddleLayout>
      <NavButton RouteTo="/ErgebnisAge">Zurück</NavButton>
      <br></br>
      <HorizStepper pageNumber={3}></HorizStepper>
    </BodyLayout>
  );
};

export default BlackBox;
