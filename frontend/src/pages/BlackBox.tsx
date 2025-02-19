import React from 'react';
import { Typography, Box, styled } from '@mui/material';

import NavButton from '@/components/buttons/Navigation';
import StyledTitle from '@/styles/StyledTitle';

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
  font-size: 0.8rem;
  color: #1a3ab8;
`;
const SecondaryHeading = styled(Typography)`
  font-family: 'Delius Unicase', cursive;
  margin: 0 0 0.5rem;
  text-align: left;
  font-size: clamp(1rem, 2vw, 1.5rem);
  color: #1a3ab8;
`;

const BlackBox: React.FC = () => {
  return (
    <Box>
      <StyledTitle>Black-Box KI</StyledTitle>
      <UpperMiddleLayout>
        <SecondaryHeading>K-nearest neighbor modell</SecondaryHeading>
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
      <NavButton RouteTo="/results-age">Zurück</NavButton>
      <br></br>
    </Box>
  );
};

export default BlackBox;
