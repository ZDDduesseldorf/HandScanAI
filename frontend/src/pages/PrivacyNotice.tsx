import { useNavigate } from 'react-router-dom';

import Header from '@/components/custom/Header';
import TextCard from '@/components/cards/WithText';
import NarrowBottomSticky from '@/components/buttons/NarrowBottomFixed';
import Centered from '@/components/layout/Centered';

export default function PrivacyNotice() {
  const navigate = useNavigate();

  return (
    <>
      <Header title="Bevor wir Beginnen..." />
      <Centered>
        <TextCard
          title="Daten statt Gebühren"
          text="Wie bei vielen digitalen Diensten gilt auch hier: Statt eines 
          klassischen Preises zahlst du mit etwas anderem – deinen Daten. In 
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
    </>
  );
}
