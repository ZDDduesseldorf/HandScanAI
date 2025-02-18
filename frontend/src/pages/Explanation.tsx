import React from 'react';
import { Box, styled, Typography } from '@mui/material';
import GeneralButton from '@/components/GeneralButton';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

import { useAppStore } from '@/store/appStore';

import Header from '@/components/custom/Header';
import WithMargins from '@/components/layout/WithMargins';
import Secondary from '@/components/headings/Secondary';
import NarrowFixedBottomRight from '@/components/buttons/NarrowFixedBottomRight';
import NearestNeighbourLayout from '@/components/custom/NearestNeighbourLayout';

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


const Explanation: React.FC = () => {
  const navigate = useNavigate();
  const capturedImage = useAppStore((state) => state.capturedImage);
  const [displayImage, setDisplayImage] = useState<string>();
  const nearestNeighbours = useAppStore((state) => state.nearestNeighbours);

  useEffect(() => {
    let objectURL: string;
    if (capturedImage) {
      fetch(capturedImage, { cache: 'no-store' })
        .then((res: Response) => res.blob())
        .then((blob: Blob) => {
          objectURL = URL.createObjectURL(blob);
          setDisplayImage(objectURL);
        })
        .catch((err: unknown) => {
          console.error('Error fetching image:', err);
        });
    }
  }, [capturedImage]);

  return (
    <WithMargins mx="2em" my="1.5em">
      <Header title="Erklärung" />
      <Secondary>
        Hier siehst du dein Bild und drei weitere die vom alter und Geschlecht
        doch gut zu deinem passen sollten, oder?
      </Secondary>
      <p>
        Hand Scan AI nutzt diese Ähnlichkeiten, um dir eine Vorhersage zu geben,
        basierend auf den Bildern, die am meisten mit deinem Bild übereinstimmen
      </p>
      <NearestNeighbourLayout src={displayImage} nearestNeighbours={nearestNeighbours}/>
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
      <NarrowFixedBottomRight onClick={() => navigate("/submission-complete")}>Weiter</NarrowFixedBottomRight>
    </WithMargins>
  );
};

export default Explanation;
