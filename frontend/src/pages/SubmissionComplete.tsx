import { useNavigate } from 'react-router-dom';

import Header from '@/components/custom/Header';
import Secondary from '@/components/headings/Secondary';
import CenteredLayout from '@/components/layout/Centered';
import Centered from '@/components/text/Centered';
import Wide from '@/components/buttons/Wide';

export default function SubmissionComplete() {
  const navigate = useNavigate();

  return (
    <>
      <Header title="Danke" />
      <CenteredLayout>
        <Secondary centered={true}>Wir hoffen du hattest Spaß!</Secondary>
        <Centered>
          Über den untenstehenden QR kannst du dir deine Ergebnisse der
          Handanalyse und weiteres Wissen zum Thema KI downloaden. HandScan AI
          hat einen eigenen Bericht für dich erstellt. Vielen Dank, dass du mit
          deiner Nutzung geholfen hast, HandScan AI zu verbessern. Bis bald!
        </Centered>
        <Wide onClick={() => navigate('/')}>Beenden</Wide>
      </CenteredLayout>
    </>
  );
}
