import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

import { useAppStore } from '@/store/appStore';

import Header from '@/components/custom/Header';
import WithMargins from '@/components/layout/WithMargins';
import Horizontal from '@/components/layout/Horizontal';
import Secondary from '@/components/headings/Secondary';
import Centered from '@/components/layout/Centered';
import NarrowFixedBottomRight from '@/components/buttons/NarrowFixedBottomRight';
import NarrowFixedBottomLeft from '@/components/buttons/NarrowFixedBottomLeft';
import NearestNeighbourLayout from '@/components/custom/NearestNeighbourLayout';

export default function Explanation() {
  const navigate = useNavigate();
  const capturedImage = useAppStore((state) => state.capturedImage);
  const [displayImage, setDisplayImage] = useState<string>();
  const nearestNeighbours = useAppStore((state) => state.nearestNeighbours);
  const scanResult = useAppStore((state) => state.scanResult);

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

  if (!scanResult) {
    return (
      <p>Keine Daten vorhanden, Bitte gehen sie zur vorherigen Seite zurück</p>
    );
  }

  return (
    <WithMargins mx="2em" my="1.5em">
      <Header title="Erklärung" />
      <Secondary>k-nearest Neighbors (k-NN): Deine Nächsten Nachbarn</Secondary>
      <p>
        Hier siehst du dein Bild und drei weitere, die vom Alter und Geschlecht
        doch gut zu deinem passen sollten, oder? HandScan AI nutzt nämlich einen
        k-NN Algorithmus, um die Vorhersage zu treffen. k-Nearest Neighbors
        (k-NN) ist eine Methode des maschinellen Lernens, die auf der Annahme
        basiert, dass ähnliche Bilder ähnliche Ergebnisse liefern.
      </p>
      <NearestNeighbourLayout
        src={displayImage}
        ageGuess={scanResult.classifiedAge}
        genderGuess={scanResult.classifiedGender}
        nearestNeighbours={nearestNeighbours}
      />
      <Centered style="max-width: 70vw;">
        <Secondary centered={true} style="margin-bottom:0">
          Statt Hand Scan AI kannst du auch k-NN Algorithmus sagen
        </Secondary>
        <p style={{ textAlign: 'center' }}>
          „k-Nearest Neighbors (k-NN)“ ist eine Methode des maschinellen
          Lernens, die auf der Annahme basiert, dass ähnliche Bilder ähnliche
          Ergebnisse liefern. Nachfolgend die wichtigsten Schritte:
        </p>
        <Horizontal margin="2em 0 1em 0">
          <img
            src="/ArrowRight.png"
            alt="Hand Scan AI Logo"
            style={{ objectFit: 'contain', alignSelf: 'start' }}
          />
          <div>
            <Secondary>Normalisierung</Secondary>
            <p>
              Die Bilder werden einheitlich angepasst und in Regionen
              unterteilt, um eine präzisere Analyse, unabhängig von der
              Handstellung, zu ermöglichen.
            </p>
          </div>
        </Horizontal>
        <Horizontal margin="1em 0">
          <img
            src="/ArrowRight.png"
            alt="Hand Scan AI Logo"
            style={{ objectFit: 'contain', alignSelf: 'start' }}
          />
          <div>
            <Secondary>Embeddings + Distanzberechnung</Secondary>
            <p>
              Das Bild wird in eine Zahlenrepräsentation umgewandelt, und die
              Ähnlichkeit wird durch die Berechnung der euklidischen Distanz
              zwischen den Bildmerkmalen bestimmt.
            </p>
          </div>
        </Horizontal>
        <Horizontal margin="1em 0">
          <img
            src="/ArrowRight.png"
            alt="Hand Scan AI Logo"
            style={{ objectFit: 'contain', alignSelf: 'start' }}
          />
          <div>
            <Secondary>Vorhersage</Secondary>
            <p>
              Die k-NN-Methode bestimmt die k ähnlichsten Bilder und leitet
              daraus eine Vorhersage ab, basierend auf der Mehrheit der nächsten
              Nachbarn.
            </p>
          </div>
        </Horizontal>
      </Centered>
      <NarrowFixedBottomLeft onClick={() => navigate(-1)}>
        Zurück
      </NarrowFixedBottomLeft>
      <NarrowFixedBottomRight onClick={() => navigate('/submission-complete')}>
        Weiter
      </NarrowFixedBottomRight>
    </WithMargins>
  );
}
