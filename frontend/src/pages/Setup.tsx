//external imports
import { useNavigate } from 'react-router-dom';

//component imports
import Centered from '@/components/layout/Centered';
import FixedButton from '@/components/buttons/NarrowFixedBottomLeft';
import WithMargins from '@/components/layout/WithMargins';
import Header from '@/components/custom/Header';

/**
 * Setup component that displays the configuration steps for setting up the camera for HandScanAI in an optimal way.
 */
export default function Setup() {
  /**
   * Method for changing the location
   * @see https://reactrouter.com/6.29.0/hooks/use-navigate
   */
  const navigate = useNavigate();

  return (
    <WithMargins mx="2em" my="1.5em">
      <Header title="Setup einrichten" />

      <div
        style={{
          display: 'flex',
          flexWrap: 'wrap',
          gap: '1em',
          justifyContent: 'center',
          marginBottom: '1em',
        }}
      >
        <img
          src="/setup/01.jpeg"
          alt="Setup 1"
          style={{ width: '100%', maxWidth: '220px', height: 'auto' }}
        />
        <img
          src="/setup/02.jpeg"
          alt="Setup 2"
          style={{ width: '100%', maxWidth: '220px', height: 'auto' }}
        />
        <img
          src="/setup/03.jpg"
          alt="Setup 3"
          style={{ width: '100%', maxWidth: '220px', height: 'auto' }}
        />
        <img
          src="/setup/04.jpg"
          alt="Setup 4"
          style={{ width: '100%', maxWidth: '220px', height: 'auto' }}
        />
      </div>

      <Centered>
        <div
          style={{
            textAlign: 'left',
            fontSize: '18px',
            lineHeight: 1.5,
            maxWidth: '600px',
            margin: '0 auto',
          }}
        >
          <div style={{ marginBottom: '1em' }}>
            <p style={{ margin: 0 }}>LogitechCapture starten</p>
            <ul style={{ margin: '0 0 0 1.25em', padding: 0 }}>
              <li style={{ margin: 0 }}>Sichtfeld 65°</li>
              <li style={{ margin: 0 }}>Zoomausschnitt anpassen</li>
              <li style={{ margin: 0 }}>
                Autofokus deaktivieren und Fokus auf 10
              </li>
            </ul>
            <p style={{ margin: 0 }}>Ziel: Bildausschnitt komplett weiß</p>
            <p style={{ margin: 0 }}>→ App schließen</p>
          </div>

          <div style={{ marginBottom: '1em' }}>
            <p style={{ margin: 0 }}>Licht auf Stufe 10</p>
            <p style={{ margin: 0 }}>Diffuser befestigt</p>
            <p style={{ margin: 0 }}>Pappe eingelegt</p>
          </div>

          <div>
            <p style={{ margin: 0 }}>Test ob Kamera erkannt wird</p>
          </div>
        </div>
      </Centered>

      <FixedButton onClick={() => void navigate('/', { state: { from: '/setup' } })}>
        Zurück
      </FixedButton>
    </WithMargins>
  );
}
