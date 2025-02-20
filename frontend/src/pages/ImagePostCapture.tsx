//external imports
import { useEffect, useState } from 'react';
import { useAppStore } from '@/store/appStore';
import { useNavigate } from 'react-router-dom';

//component imports
import WithMargins from '@/components/layout/WithMargins';
import Header from '@/components/custom/Header';
import Secondary from '@/components/headings/Secondary';
import Horizontal from '@/components/layout/Horizontal';
import Centered from '@/components/layout/Centered';
import Wide from '@/components/buttons/Wide';

/**
 * On this page, the user is shown the picture they have taken with a short
 * explanatory text. The user has the option of starting the analysis with
 * this image or capturing a new one.
 *
 * @returns Page which shows the user their captured image
 */
export default function ImagePostCapture() {
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
  ] = useState<string | null>(null);

  // Ensure that the image is fetched when the page is loaded to make sure that the image preview is not using a previous cached image
  useEffect(() => {
    let objectURL: string | undefined;
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
    return () => {
      if (objectURL) {
        URL.revokeObjectURL(objectURL);
      }
    };
  }, [capturedImage]);

  return (
    <WithMargins mx="2em" my="1.5em">
      <Header title="Bildaufnahme" />
      <Secondary>Wir haben ein Foto für dich und HandScanAI!</Secondary>
      <p>
        Das Foto wird zu unserem Datensatz hinzugefügt, der mit jeder neuen
        Aufnahme wächst.
      </p>
      <p>
        Warum ist das so wichtig? Künstliche Intelligenz wird durch Daten
        trainiert. Je mehr Daten vorhanden sind, desto besser kann die KI Muster
        erkennen, Zusammenhänge verstehen und präzisere Vorhersagen treffen.
        Dein Foto trägt also dazu bei, dass HandScan AI nicht nur intelligenter,
        sondern auch vielfältiger und gerechter wird - denn ein breiter
        Datensatz hilft, Vorurteile (Bias) zu reduzieren.
      </p>
      <Centered>
        {displayImage ? (
          <img
            src={displayImage}
            alt="Captured"
            style={{ maxHeight: '180px', objectFit: 'contain', margin: '1em' }}
          />
        ) : (
          <p>Image is loading</p>
        )}
      </Centered>
      <Horizontal>
        <img
          src="/ArrowRight.png"
          alt="Hand Scan AI Logo"
          style={{
            objectFit: 'contain',
            alignSelf: 'center',
            height: '25px',
          }}
        />
        <p style={{ fontSize: '1.25em' }}>
          Klicke auf &quot;Analyse starten&quot;, um herauszufinden, was
          HandScan AI über deine Hand verrät!
        </p>
      </Horizontal>
      <Horizontal style="justify-content: center; margin-top: 1em;">
        <Wide
          onClick={() => void navigate('/image-capture')}
          variant="outlined"
        >
          Neu aufnehmen
        </Wide>
        <Wide onClick={() => void navigate('/processing')}>
          Analyse starten
        </Wide>
      </Horizontal>
    </WithMargins>
  );
}
