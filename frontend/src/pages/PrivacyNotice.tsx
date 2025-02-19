//external imports
import { useNavigate } from 'react-router-dom';

//component imports
import Header from '@/components/custom/Header';
import TextCard from '@/components/cards/WithText';
import NarrowBottomSticky from '@/components/buttons/NarrowFixedBottomRight';
import Centered from '@/components/layout/Centered';
import WithMargins from '@/components/layout/WithMargins';

/**
 * Shows the user a short text informing them about data privacy issues. 
 * A button can be used to navigate to the next page.
 * 
 * @returns Page showing a simple informative text
 */
export default function PrivacyNotice() {
  /**
   * Method for changing the location
   * @see https://reactrouter.com/6.29.0/hooks/use-navigate
   */
  const navigate = useNavigate();

  return (
    <WithMargins mx="2em" my="1.5em">
      <Header title="Bevor wir Beginnen..." />
      <Centered>
        <TextCard
          title="Daten statt Gebühren"
          text="Wie bei vielen digitalen Diensten gilt auch hier: Statt eines 
          klassischen Preises zahlst du mit etwas anderem - deinen Daten. In 
          unserer App sind es vor allem deine Interaktionen und die Bilder deiner 
          Hand, die die KI verarbeitet und lernen lassen. Diese Daten sind der 
          „Treibstoff“, der der KI hilft, intelligenter, präziser und 
          anpassungsfähiger zu werden. Mit deinen Eingaben trägst du aktiv dazu 
          bei, dass das System weiterentwickelt und optimiert wird, um dir und 
          anderen Nutzern zukünftig noch bessere Ergebnisse zu bieten. "
        />
      </Centered>
      <NarrowBottomSticky onClick={() => navigate('/image-capture')}>
        Weiter
      </NarrowBottomSticky>
    </WithMargins>
  );
}
