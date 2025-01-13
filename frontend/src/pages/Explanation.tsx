import React from 'react';
import { Box, Button, styled, Typography } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import StyledTitle from '@/styles/StyledTitle';
import NavButton from '@/components/NavButton';

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
const MiddlePageLayout = styled(Typography)`
  display: grid;
`;

const Explanation: React.FC = () => {
  const navigate = useNavigate();

  return (
    <Box>
      <StyledTitle>Erklärung</StyledTitle>
      <SecondaryHeading>
        Hier siehst du dein Bild und drei weitere die vom alter und Geschlcht
        doch gut zu dinEm passen sollten, oder?
      </SecondaryHeading>
      <BoxText>
        Hand Scan AI nutzt diese Ähnlichkeiten, um dir eine Vorhersage zu geben,
        basierend auf den Bildern, die am meisten mit deinem Bild übereinstimmen
      </BoxText>
      <div></div>
      <SecondaryHeading>
        Statt Hand Scan AI kannst du auch k-NN Algorithmus sagen
      </SecondaryHeading>
      <BoxText>
        „k-Nearest Neighbors (k-NN)“ ist eine Methode des maschinellen Lernens,
        die auf der Annahme basiert, dass ähnliche Bilder ähnliche Ergebnisse
        liefern. Nachfolgend die wichtigsten Schritte:
      </BoxText>
      <MiddlePageLayout></MiddlePageLayout>
      <SecondaryHeading>Mehr zur KI</SecondaryHeading>
      <BoxText>
        Klicke hier, um mehr über die „Black Box KI“ zu erfahren und den
        zugrunde liegenden Algorithmus zu entdecken und Fachbegriffe
        wie Embeddings kennenzulernen, die für die Vorhersagen wichtig sind.
      </BoxText>
      <SecondaryHeading>
        Körperliche Merkmale und ihre Bedeutung
      </SecondaryHeading>
      <BoxText>
        Was bestimmt eigentlich das Geschlecht und Alter einer Hand? Klicke auf
        “Weiter”, um mehr darüber zu erfahren, welche körperlichen Merkmale
        dabei eine Rolle spielen und wie diese in die Vorhersage einfließen.
      </BoxText>

      <Button
        variant="contained"
        color="primary"
        onClick={() => navigate('/blackbox')}
      >
        Erklärung
      </Button>
      {/* <NavButton>Erfahre mehr über Ki</NavButton> */}
      <NavButton RouteTo="/results-gender">Weiter</NavButton>
    </Box>
  );
};

export default Explanation;
