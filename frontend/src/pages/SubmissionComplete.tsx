//external imports
import { useNavigate } from 'react-router-dom';

//component imports
import Header from '@/components/custom/Header';
import Secondary from '@/components/headings/Secondary';
import Centered from '@/components/layout/Centered';
import WithMargins from '@/components/layout/WithMargins';
import NarrowFixedBottomMiddle from '@/components/buttons/NarrowFixedBottomMiddle';

/**
 * Displays a simple thank you text and a button to return to the home page after
 * using the application.
 *
 * @returns Page showing a thank you text for using the application
 */
export default function SubmissionComplete() {
  /**
   * Method for changing the location
   * @see https://reactrouter.com/6.29.0/hooks/use-navigate
   */
  const navigate = useNavigate();

  return (
    <WithMargins mx="2em" my="1.5em">
      <Header title="Danke" />
      <Centered style="text-align:center;">
        <Secondary centered={true}>Wir hoffen du hattest Spaß!</Secondary>
        <p>
          Du möchtest deine Ergbnisse dir zu Hause noch mal in Ruhe durchlesen
          und dein Wissen über Normalisierung, Embeddings und Vorhersagen
          auffrischen, kein Problem, HandScan AI hat einen eigenen Bericht für
          dich erstellt. Wende dich dazu bitte an den Betreuer von HandScan AI
          und du kannst den Bericht per E-Mail erhalten.
        </p>
        <p>
          Vielen Dank, dass du mit deiner Nutzung geholfen hast, HandScan AI zu
          verbessern. Bis bald!
        </p>
        <NarrowFixedBottomMiddle onClick={() => navigate('/')}>
          Beenden
        </NarrowFixedBottomMiddle>
      </Centered>
    </WithMargins>
  );
}
