//external imports
import { useNavigate } from 'react-router-dom';

//component imports
import Header from '@/components/custom/Header';
import Secondary from '@/components/headings/Secondary';
import Centered from '@/components/layout/Centered';
import WithMargins from '@/components/layout/WithMargins';
import FixedBottomMiddle from '@/components/buttons/FixedBottomMiddle';

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
          Du möchtest die Erklärungen noch einmal in Ruhe durchgehen und dein
          Wissen über Normalisierung, Embeddings und Vorhersagen vertiefen? Kein
          Problem! HandScan AI bietet detailliertere Informationen zu diesen
          Themen, einschließlich weiterer Begriffe und der genutzten Schritte.
          Über den QR-Code gelangst du direkt zu unserem Git-Repo, wo du eine
          PDF herunterladen kannst.
        </p>
        <p>
          Vielen Dank, dass du mit deiner Nutzung geholfen hast, HandScan AI zu
          verbessern. Bis bald!
        </p>
        <FixedBottomMiddle onClick={() => void navigate('/')}>
          Beenden
        </FixedBottomMiddle>
      </Centered>
    </WithMargins>
  );
}
