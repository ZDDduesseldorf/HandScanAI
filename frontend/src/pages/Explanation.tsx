import React from 'react';
import { Box, Button, styled, Typography } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import StyledTitle from '@/styles/StyledTitle';
import NavButton from '@/components/NavButton';
import GeneralButton from '@/components/GeneralButton';

const BoxText = styled(Typography)`
  font-family: 'Poppins', sans-serif;
  margin: 0 0 1 rem;
  text-align: justify;
  font-size: 1.2rem;
  color: #000000;
`;
const SecondaryHeading = styled(Typography)`
  font-family: 'Delius Unicase', cursive;
  // margin: 0 0 0.5rem;
  margin-top: 1.5rem;

  text-align: left;
  font-size: clamp(1rem, 2vw, 1.5rem);
  color: #000000;
`;
const HandGalleryLayout = styled(Typography)`
  display: flex;
  flex-direction: row;
`;
const HandImgLayout = styled(Typography)`
  display: flex;
  flex-direction: column;
`;

const Explanation: React.FC = () => {
  // const navigate = useNavigate();

  return (
    <Box>
      <StyledTitle>Erklärung</StyledTitle>
      <SecondaryHeading>
        Hier siehst du dein Bild und drei weitere die vom alter und Geschlecht
        doch gut zu deinem passen sollten, oder?
      </SecondaryHeading>
      <BoxText>
        Hand Scan AI nutzt diese Ähnlichkeiten, um dir eine Vorhersage zu geben,
        basierend auf den Bildern, die am meisten mit deinem Bild übereinstimmen
      </BoxText>
      <div></div>
      <SecondaryHeading style={{ textAlign: 'center' }}>
        Statt Hand Scan AI kannst du auch k-NN Algorithmus sagen
      </SecondaryHeading>
      <BoxText style={{ textAlign: 'center' }}>
        „k-Nearest Neighbors (k-NN)“ ist eine Methode des maschinellen Lernens,
        die auf der Annahme basiert, dass ähnliche Bilder ähnliche Ergebnisse
        liefern. Nachfolgend die wichtigsten Schritte:
      </BoxText>
      <HandGalleryLayout></HandGalleryLayout>
      <SecondaryHeading>Mehr zur KI</SecondaryHeading>
      <BoxText>
        Klicke hier, um mehr über die „Black Box KI“ zu erfahren und den
        zugrunde liegenden Algorithmus zu entdecken und Fachbegriffe
        wie Embeddings kennenzulernen, die für die Vorhersagen wichtig sind.
      </BoxText>
      <GeneralButton RouteTo="/results-age">Erfahre mehr über Ki</GeneralButton>

      <SecondaryHeading>
        Körperliche Merkmale und ihre Bedeutung
      </SecondaryHeading>
      <BoxText>
        Was bestimmt eigentlich das Geschlecht und Alter einer Hand? Klicke auf
        “Weiter”, um mehr darüber zu erfahren, welche körperlichen Merkmale
        dabei eine Rolle spielen und wie diese in die Vorhersage einfließen.
      </BoxText>

      <GeneralButton RouteTo="/blackbox">Erklärung</GeneralButton>
      <NavButton RouteTo="/results-gender">Weiter</NavButton>
    </Box>
  );
};

export default Explanation;
