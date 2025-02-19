import { Box, Typography } from '@mui/material';
import { styled } from '@mui/material/styles';
import { useEffect, useRef, useState } from 'react';
import { useAppStore } from '@/store/appStore';
import { useNavigate } from 'react-router-dom';
import WithMargins from '@/components/layout/WithMargins';
import Header from '@/components/custom/Header';
import Secondary from '@/components/headings/Secondary';
import Horizontal from '@/components/layout/Horizontal';

interface ServerMessage {
  flow: string;
  message?: string;
  landmarks_detected?: boolean;
  hand_is_spread?: boolean;
  hand_is_visible?: boolean;
  time?: number;
  image?: string;
}

const Container = styled(Box)`
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  width: 80%;
  margin: 0 auto;
  padding: 1em;
  background-color: #f0f0f0;
  border-radius: 12px;
`;

const VideoWrapper = styled(Box)`
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 50vh;
`;

const Video = styled('video')`
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 8px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.25);
`;

const InfoSection = styled(Box)`
  flex: 2;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding-left: 20px;
`;

const InstructionBox = styled(Box)`
  width: 100%;
  height: 80px;
  margin-top: 20px;
  border: 2px solid #ccc;
  border-radius: 8px;
  background-color: white;
  color: black;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
`;

export default function ImageCapture() {
  const navigate = useNavigate();
  const scanEntry = useAppStore((state) => state.scanEntry);
  const updateCapturedImage = useAppStore((state) => state.setCapturedImage);
  const videoRef = useRef<HTMLVideoElement>(null);
  const wsRef = useRef<WebSocket | null>(null);
  const [instruction, setInstruction] = useState('Kamera wird vorbereitet...');

  useEffect(() => {
    if (!scanEntry?.id) {
      console.error('Ungültige Scan-Eintrags-ID.');
      alert(
        'Scan-Eintrags-ID fehlt oder ist ungültig. Bitte starte den Prozess neu.',
      );
      navigate('/');
      return;
    }

    const currentVideoRef = videoRef.current;
    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d');

    const ws = new WebSocket(`ws://localhost:8000/ws/${scanEntry.id}`);
    wsRef.current = ws;

    let interval: ReturnType<typeof setInterval>;

    ws.onopen = () => {
      navigator.mediaDevices
        .getUserMedia({
          video: {
            width: { ideal: 4096 },
            height: { ideal: 2160 },
          },
        })
        .then((stream) => {
          if (currentVideoRef) {
            currentVideoRef.srcObject = stream;
            currentVideoRef.play().catch((error) => {
              console.error('Fehler beim Abspielen des Videos:', error);
            });

            currentVideoRef.onloadedmetadata = () => {
              const videoWidth = currentVideoRef.videoWidth;
              const videoHeight = currentVideoRef.videoHeight;
              canvas.width = videoWidth;
              canvas.height = videoHeight;

              interval = setInterval(() => {
                if (context && currentVideoRef) {
                  context.drawImage(
                    currentVideoRef,
                    0,
                    0,
                    canvas.width,
                    canvas.height,
                  );
                  canvas.toBlob((blob) => {
                    if (blob && ws.readyState === WebSocket.OPEN) {
                      ws.send(blob);
                    }
                  }, 'image/jpeg');
                }
              }, 333);
            };
          }
        })
        .catch((error) => {
          setInstruction('Fehler beim Zugriff auf die Kamera.');
          console.error('Fehler beim Zugriff auf die Kamera:', error);
        });
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data as string) as ServerMessage;

        switch (data.flow) {
          case 'validation':
            setInstruction(
              data.landmarks_detected
                ? 'Hand erkannt. Warte auf die Bedingungen...'
                : 'Bitte platziere deine Hand im Kamerarahmen.',
            );
            break;
          case 'timer':
            setInstruction(`Foto wird in ${data.time} Sekunden aufgenommen...`);
            break;
          case 'taking_images':
            setInstruction('Bild wird aufgenommen...');
            break;
          case 'success':
            setInstruction('Bild erfolgreich aufgenommen!');
            updateCapturedImage(data.image!);
            setTimeout(() => navigate('/image-post-capture'), 1000);
            break;
          case 'error':
            setInstruction(`Fehler: ${data.message}`);
            break;
          default:
            setInstruction('Warte auf weitere Anweisungen...');
        }
      } catch {
        setInstruction('Fehler beim Verarbeiten der Server-Antwort.');
      }
    };

    ws.onclose = () => {
      console.log('WebSocket-Verbindung geschlossen');
      if (currentVideoRef?.srcObject) {
        const tracks = (currentVideoRef.srcObject as MediaStream).getTracks();
        tracks.forEach((track) => track.stop());
      }
    };

    return () => {
      // Stop the interval
      clearInterval(interval);

      // Stop the video stream
      if (currentVideoRef?.srcObject) {
        const tracks = (currentVideoRef.srcObject as MediaStream).getTracks();
        tracks.forEach((track) => track.stop());
      }

      // Close the WebSocket connection
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [scanEntry?.id, navigate, updateCapturedImage]);

  return (
    <WithMargins mx="2em" my="1.5em">
      <Header title="Bildaufnahme" />
      <Container>
        <VideoWrapper>
          <Video ref={videoRef} autoPlay playsInline />
        </VideoWrapper>
        <InfoSection>
          <Secondary>Positionierung</Secondary>
          <p style={{ fontSize: '1.25em' }}>
            HandScan AI nimmt automatisch Bilder deiner Hand auf. Sobald die
            Kamera eine Hand erkennt, wird der Countdown gestartet.
          </p>
          <Horizontal>
            <img
              src="/ArrowRight.png"
              alt="Hand Scan AI Logo"
              style={{
                objectFit: 'contain',
                alignSelf: 'center',
                height: ' 25px',
              }}
            />
            <p style={{ fontSize: '1.25em' }}>
              Bitte lege deine Hand mit der Handfläche nach unten in die
              Fotobox.
            </p>
          </Horizontal>
          <Horizontal>
            <img
              src="/ArrowRight.png"
              alt="Hand Scan AI Logo"
              style={{
                objectFit: 'contain',
                alignSelf: 'center',
                height: ' 25px',
              }}
            />
            <p style={{ fontSize: '1.25em' }}>
              Es ist egal, ob du die rechte oder linke Hand nimmst.
            </p>
          </Horizontal>
          <InstructionBox>
            <Typography>{instruction}</Typography>
          </InstructionBox>
        </InfoSection>
      </Container>
    </WithMargins>
  );
}
