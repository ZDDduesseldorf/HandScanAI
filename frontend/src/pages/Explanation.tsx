import React from 'react';
import { Box, styled, Typography } from '@mui/material';
import StyledTitle from '@/styles/StyledTitle';
import NavButton from '@/components/buttons/Navigation';
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
const HorizImageBox = styled(Box)`
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  margin-top: 20px;
  // objectFit: contain;
}
`;

const ArrowTextBox = styled(Box)`
  display: flex;
  flex-direction: row;
  justify-content:start;
}
`;
const VerticalElements = styled(Box)`
  display: flex;
  flex-direction: column;
  justify-content: center;
}
`;
const HandText = styled(Box)`
font-family: 'Delius Unicase', cursive;
margin-top: 1.5rem;
text-align: left;
font-size: clamp(0.5rem, 2vw, 1rem);
color: #0F3EB5;
}
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
      <HorizImageBox>
        <VerticalElements>
          <img src="/Hand.png" alt="Hand Scan AI Logo" />
          <HandText>
            Dein Bild: <br></br> Weiblich, 28
          </HandText>
        </VerticalElements>
        <img src="/ArrowRight.png" alt="Hand Scan AI Logo" />
        <VerticalElements>
          <img src="/Hand.png" />
          <HandText>Männlich, 23</HandText>
        </VerticalElements>
        <VerticalElements>
          <img src="/Hand.png" />
          <HandText>Weiblich, 20</HandText>
        </VerticalElements>
        <VerticalElements>
          <img src="/Hand.png" />
          <HandText>Männlich, 19</HandText>
        </VerticalElements>
      </HorizImageBox>
      <SecondaryHeading style={{ textAlign: 'center' }}>
        Statt Hand Scan AI kannst du auch k-NN Algorithmus sagen
      </SecondaryHeading>
      <BoxText style={{ textAlign: 'center' }}>
        „k-Nearest Neighbors (k-NN)“ ist eine Methode des maschinellen Lernens,
        die auf der Annahme basiert, dass ähnliche Bilder ähnliche Ergebnisse
        liefern. Nachfolgend die wichtigsten Schritte:
      </BoxText>
      <ArrowTextBox>
        <img src="/ArrowRight.png" alt="Hand Scan AI Logo" />
        <VerticalElements>
          <SecondaryHeading>Normalisierung </SecondaryHeading>
          <BoxText>
            Bevor die Bilder miteinander verglichen werden, müssen sie
            normalisiert werden. Das bedeutet, dass die Daten so umgewandelt
            werden, dass sie alle auf der gleichen Skala sind.
          </BoxText>
        </VerticalElements>
      </ArrowTextBox>
      <ArrowTextBox>
        <img src="/ArrowRight.png" alt="Hand Scan AI Logo" />
        <VerticalElements>
          <SecondaryHeading>Distanzberechnung </SecondaryHeading>
          <BoxText>
            Um herauszufinden, welche Bilder am ähnlichsten sind, wird die
            Distanz zwischen den Merkmalen des Bildes und den anderen Bildern
            berechnet. Dies geschieht mit mathematischen Methoden, wie der
            euklidischen Distanz, die misst, wie „weit“ ein Bild von einem
            anderen entfernt ist. Je kleiner die Distanz, desto ähnlicher sind
            sich die Bilder.
          </BoxText>
        </VerticalElements>
      </ArrowTextBox>
      <ArrowTextBox>
        <img src="/ArrowRight.png" alt="Hand Scan AI Logo" />
        <VerticalElements>
          <SecondaryHeading>Vorhersagen </SecondaryHeading>
          <BoxText>
            Nachdem die Entfernungen berechnet wurden, wählt die k-NN-Methode
            die nächsten Nachbarn (also die k ähnlichsten Bilder) aus und trifft
            eine Vorhersage. Zum Beispiel, wenn die meisten der nächsten
            Nachbarn ein bestimmtes Geschlecht oder Alter haben, wird dieses
            auch für das Bild vorhergesagt. Die Vorhersage basiert also auf der
            Mehrheit der „nächsten Nachbarn“.
          </BoxText>
        </VerticalElements>
      </ArrowTextBox>
      <SecondaryHeading>Mehr zur KI</SecondaryHeading>
      <BoxText>
        Klicke hier, um mehr über die „Black Box KI“ zu erfahren und den
        zugrunde liegenden Algorithmus zu entdecken und Fachbegriffe wie
        Embeddings kennenzulernen, die für die Vorhersagen wichtig sind.
      </BoxText>
      <div style={{ textAlign: 'left', marginTop: 15 }}>
        <GeneralButton RouteTo="/results-age">
          Erfahre mehr über Ki
        </GeneralButton>
      </div>

      <SecondaryHeading>
        Körperliche Merkmale und ihre Bedeutung
      </SecondaryHeading>
      <BoxText>
        Was bestimmt eigentlich das Geschlecht und Alter einer Hand? Klicke auf
        “Weiter”, um mehr darüber zu erfahren, welche körperlichen Merkmale
        dabei eine Rolle spielen und wie diese in die Vorhersage einfließen.
      </BoxText>
      <div style={{ textAlign: 'left', marginTop: 15 }}>
        <GeneralButton RouteTo="/blackbox">Erklärung</GeneralButton>
      </div>
      <NavButton RouteTo="/results-gender">Weiter</NavButton>
    </Box>
  );
};

export default Explanation;
