//external imports
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

//internal imports
import { useAppStore } from '@/store/appStore';

//component imports
import Header from '@/components/custom/Header';
import WithMargins from '@/components/layout/WithMargins';
import Horizontal from '@/components/layout/Horizontal';
import Secondary from '@/components/headings/Secondary';
import Centered from '@/components/layout/Centered';
import NarrowFixedBottomRight from '@/components/buttons/NarrowFixedBottomRight';
import NarrowFixedBottomLeft from '@/components/buttons/NarrowFixedBottomLeft';
import NearestNeighbourLayout from '@/components/custom/NearestNeighbourLayout';

/**
 * A page that presents the explanation for the classification. Three of the
 * nearest neighbors are shown on the page and a small explanatory text is
 * displayed that briefly explains the procedure.
 *
 * @returns Page with nearest neighbours and explanatory text
 */
export default function Explanation() {
  /**
   * Method for changing the location
   * @see https://reactrouter.com/6.29.0/hooks/use-navigate
   */
  const navigate = useNavigate();

  /**
   * The captured image of the user stored in the React app store.
   */
  const capturedImage = useAppStore((state) => state.capturedImage);

  const [
    /**
     * The image that is displayed on the page
     */
    displayImage,
    /**
     * Saves the image to be displayed when the captured image is retrieved
     * from the store.
     */
    setDisplayImage,
  ] = useState<string>();

  /**
   * The nearest neighbours stored in the React app store
   */
  const nearestNeighbours = useAppStore((state) => state.nearestNeighbours);

  /**
   * The scan result stored in the React app store
   */
  const scanResult = useAppStore((state) => state.scanResult);

  // Update the displayImage when the captured image is retrieved from the
  // store. Log the error in the console if there is one.
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

  // If there is no result, the explanation cannot be displayed. The user should
  // then navigate to another page.
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
        doch gut zu deinem passen sollten, oder? HandScan AI gibt dir eine
        Vorhersage, basierend auf den Bildern, die in unserem Datensatz, am
        meisten mit deinem Bild übereinstimmen. HandScan AI nutzt nämlich einen
        k-Nearest Neighbors (k-NN) Algorithmus, um die Vorhersage zu treffen.
      </p>
      <NearestNeighbourLayout
        src={displayImage}
        ageGuess={scanResult.classifiedAge}
        genderGuess={scanResult.classifiedGender}
        nearestNeighbours={nearestNeighbours}
      />
      <Centered style="max-width: 70vw;">
        <Secondary centered={true} style="margin-bottom:0">
          Vom Bild zur Vorhersage: Die Schritte hinter HandScan AI
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
            <img
              src="/explanation/explanation_1.jpeg"
              alt="explanatory image"
              style={{ objectFit: 'contain', maxWidth: '80vw', width: '95%' }}
            />
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
            <img
              src="/explanation/explanation_2.jpeg"
              alt="explanatory image"
              style={{ objectFit: 'contain', maxWidth: '80vw', width: '95%' }}
            />
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
            <img
              src="/explanation/explanation_3.jpeg"
              alt="explanatory image"
              style={{ objectFit: 'contain', maxWidth: '80vw', width: '95%' }}
            />
          </div>
        </Horizontal>
      </Centered>
      <NarrowFixedBottomLeft onClick={() => void navigate(-1)}>
        Zurück
      </NarrowFixedBottomLeft>
      <NarrowFixedBottomRight
        onClick={() => void navigate('/submission-complete')}
      >
        Weiter
      </NarrowFixedBottomRight>
    </WithMargins>
  );
}
