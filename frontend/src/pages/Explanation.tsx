import React from 'react';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

import { useAppStore } from '@/store/appStore';

import Header from '@/components/custom/Header';
import WithMargins from '@/components/layout/WithMargins';
import Horizontal from '@/components/layout/Horizontal';
import Secondary from '@/components/headings/Secondary';
import NarrowFixedBottomRight from '@/components/buttons/NarrowFixedBottomRight';
import Wide from '@/components/buttons/Wide';
import NearestNeighbourLayout from '@/components/custom/NearestNeighbourLayout';

const Explanation: React.FC = () => {
  const navigate = useNavigate();
  const capturedImage = useAppStore((state) => state.capturedImage);
  const [displayImage, setDisplayImage] = useState<string>();
  const nearestNeighbours = useAppStore((state) => state.nearestNeighbours);
  const scanResult = useAppStore((state) => state.scanResult);
    
  if (!scanResult) {
    return (
      <p>Keine Daten vorhanden, Bitte gehen sie zur vorherigen Seite zurück</p>
    );
  }

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
        basierend auf den Bildern, die am meisten mit deinem Bild übereinstimmen. 
        Es kann sein, dass du hier im Vergleich die gleiche Hand öfters siehst. 
        Woran das liegen kann, kannst du weiter unten lesen.
      </p>
      <NearestNeighbourLayout 
        src={displayImage} 
        ageGuess={scanResult.classifiedAge} 
        genderGuess={scanResult.classifiedGender} 
        nearestNeighbours={nearestNeighbours}/>
      <Secondary>
        Statt Hand Scan AI kannst du auch k-NN Algorithmus sagen
      </Secondary>
      <p>„k-Nearest Neighbors (k-NN)“ ist eine Methode des maschinellen Lernens,
      die auf der Annahme basiert, dass ähnliche Bilder ähnliche Ergebnisse
      liefern. Nachfolgend die wichtigsten Schritte:</p>
      <Horizontal>
        <img src="/ArrowRight.png" alt="Hand Scan AI Logo" style={{ objectFit: 'contain', alignSelf: 'start'}}/>
        <div>
          <Secondary>Normalisierung </Secondary>
          <p>
          Bevor die Bilder miteinander verglichen werden, müssen sie normalisiert 
          werden. Das bedeutet, dass die Daten so umgewandelt werden, dass sie alle 
          auf der gleichen Skala sind. Gleichzeitig unterteilen wir dein Handbild 
          in verschidene Regionen wie Daumen und Mittelfinger, um Merkmale 
          detaillierter analysieren zu können und deine Handstellung das Ergebnis 
          nicht beeinflusst. 
          </p>
        </div>
      </Horizontal>
      <Horizontal>
        <img src="/ArrowRight.png" alt="Hand Scan AI Logo" style={{ objectFit: 'contain', alignSelf: 'start'}}/>
        <div>
          <Secondary>Embeddings + Distanzberechnung</Secondary>
          <p>
          uerst wird dein Bild als eine Zahlenrepräsentation (Embedding) umgewandelt, 
          damit es vom Algorithmus besser gelesen und verarbeitet werden kann. Um 
          herauszufinden, welche Bilder am ähnlichsten sind, wird die Distanz zwischen 
          den Merkmalen des Bildes und den anderen Bildern berechnet. Dies geschieht 
          mit mathematischen Methoden, wie der euklidischen Distanz, die misst, wie 
          „weit“ ein Bild von einem anderen entfernt ist. Je kleiner die Distanz, 
          desto ähnlicher sind sich die Bilder.
          </p>
        </div>
      </Horizontal>
      <Horizontal>
        <img src="/ArrowRight.png" alt="Hand Scan AI Logo" style={{objectFit: 'contain', alignSelf: 'start'}}/>
        <div>
          <Secondary>Vorhersage</Secondary>
          <p>
          Nachdem die Entfernungen berechnet wurden, wählt die k-NN-Methode die 
          nächsten Nachbarn (also die k ähnlichsten Bilder) aus und trifft eine 
          Vorhersage. Zum Beispiel, wenn die meisten der nächsten Nachbarn ein 
          bestimmtes Geschlecht oder Alter haben, wird dieses auch für din Bild 
          vorhergesagt. Die Vorhersage basiert also auf der Mehrheit der „nächsten 
          Nachbarn“. Wenn du oder deine nächsten Nachbarn schon mal HandScan AI genutzt, 
          dann kann es deshalb vorkommen, dass du die gleichen Hände im Vergleich siehst, 
          da deine Hand sich selbst natürlich im besten Fall am ähnlichsten ist. 
          </p>
        </div>
      </Horizontal>
      <Secondary>Mehr zur KI</Secondary>
      <p>
        Klicke hier, um mehr über die „Black Box KI“ zu erfahren und den
        zugrunde liegenden Algorithmus zu entdecken und Fachbegriffe wie
        Embeddings kennenzulernen, die für die Vorhersagen wichtig sind.
      </p>
      <Wide onClick={() => navigate("/blackbox")}>Erfahre mehr über KI</Wide>
      <NarrowFixedBottomRight onClick={() => navigate("/submission-complete")}>Weiter</NarrowFixedBottomRight>
    </WithMargins>
  );
};

export default Explanation;
