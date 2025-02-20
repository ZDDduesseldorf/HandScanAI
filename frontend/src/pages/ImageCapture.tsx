//external imports
import { useEffect, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Box, Typography } from '@mui/material';
import { styled } from '@mui/material/styles';

//internal imports
import { useAppStore } from '@/store/appStore';

//component imports
import Header from '@/components/custom/Header';
import Secondary from '@/components/headings/Secondary';
import Horizontal from '@/components/layout/Horizontal';

/**
 * Interface representing messages received from the backend WebSocket.
 *
 * The backend (see `backend/app/api/websocket.py`) sends messages with these flows:
 *
 * - error:
 *     {
 *       "flow": "error",
 *       "message": string // Error message
 *     }
 *
 * - validation:
 *     {
 *       "flow": "validation",
 *       "landmarks_detected": boolean,
 *       "hand_is_spread": boolean,
 *       "hand_is_visible": boolean
 *     }
 *
 * - timer:
 *     {
 *       "flow": "timer",
 *       "time": number // Seconds remaining before capture
 *     }
 *
 * - taking_images:
 *     {
 *       "flow": "taking_images"
 *     }
 *
 * - success:
 *     {
 *       "flow": "success",
 *       "image": string // URL to the saved image
 *     }
 */
interface ServerMessage {
  /** The current flow stage of the process (e.g., 'validation', 'timer', etc.). */
  flow: string;
  /** Optional message string provided by the server (typically for error or info). */
  message?: string;
  /** Flag indicating if landmarks were detected in the image. */
  landmarks_detected?: boolean;
  /** Flag indicating if the hand is spread. */
  hand_is_spread?: boolean;
  /** Flag indicating if the hand is visible. */
  hand_is_visible?: boolean;
  /** Countdown time in seconds before image capture (if applicable). */
  time?: number;
  /** The captured image data as a base64 string or URL (if applicable). */
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
  text-align: left;
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
  object-fit: contain;
  transform: rotate(-90deg);
  border-radius: 8px;
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

/**
 * Handles capturing video frames from the user's webcam, sending them via a WebSocket to the backend, and interpreting the responses.
 * See `backend/app/api/websocket.py` for the corresponding backend API.
 * @returns Page for taking a hand image
 */
export default function ImageCapture() {
  /**
   * Method for changing the location
   * @see https://reactrouter.com/6.29.0/hooks/use-navigate
   */
  const navigate = useNavigate();

  /**
   * The scan entry stored in the React app store
   */
  const scanEntry = useAppStore((state) => state.scanEntry);

  /**
   * The URL to the captured image stored in the React app store
   */
  const updateCapturedImage = useAppStore((state) => state.setCapturedImage);

  /**
   * Reference to the video element in the DOM
   */
  const videoRef = useRef<HTMLVideoElement>(null);

  /**
   * Reference to the WebSocket connection
   */
  const wsRef = useRef<WebSocket | null>(null);

  /**
   * State for displaying the current instruction message
   */
  const [instruction, setInstruction] = useState('Kamera wird vorbereitet...');

  useEffect(() => {
    // Validate the scan entry ID, and return to the home page if it's invalid
    if (!scanEntry?.id) {
      console.error('Ungültige Scan-Eintrags-ID.');
      alert(
        'Scan-Eintrags-ID fehlt oder ist ungültig. Bitte starte den Prozess neu.',
      );
      void navigate('/');
      return;
    }

    // Get the current video element and create a canvas for capturing frames
    const currentVideoRef = videoRef.current;
    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d');

    // Establish the WebSocket connection with the backend
    const ws = new WebSocket(`ws://localhost:8000/ws/${scanEntry.id}`);
    wsRef.current = ws;

    let interval: ReturnType<typeof setInterval>;

    // When the WebSocket connection is opened, start the video stream
    ws.onopen = () => {
      // Request access to the user's camera
      navigator.mediaDevices
        .getUserMedia({
          video: {
            width: { ideal: 4096 },
            height: { ideal: 2160 },
          },
        })
        .then((stream) => {
          if (currentVideoRef) {
            // Attach the stream to the video element and start playback
            currentVideoRef.srcObject = stream;
            currentVideoRef.play().catch((error) => {
              console.error('Fehler beim Abspielen des Videos:', error);
            });

            // Once video metadata is loaded, configure the canvas and begin frame capture
            currentVideoRef.onloadedmetadata = () => {
              const videoWidth = currentVideoRef.videoWidth;
              const videoHeight = currentVideoRef.videoHeight;
              canvas.width = videoWidth;
              canvas.height = videoHeight;

              // Capture frames at a rate of 3 frames per second
              interval = setInterval(() => {
                if (context && currentVideoRef) {
                  context.drawImage(
                    currentVideoRef,
                    0,
                    0,
                    canvas.width,
                    canvas.height,
                  );
                  // Convert the frame to a JPEG blob and send it to the backend
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
          // Display an error message if camera access is denied
          setInstruction('Fehler beim Zugriff auf die Kamera.');
          console.error('Fehler beim Zugriff auf die Kamera:', error);
        });
    };

    // Handle messages received from the WebSocket
    ws.onmessage = (event) => {
      try {
        // Parse the JSON message from the backend
        const data = JSON.parse(event.data as string) as ServerMessage;

        // Interpret the backend flow and update UI instructions accordingly
        switch (data.flow) {
          case 'validation':
            // If validation fails, instruct the user to adjust hand position.
            // When landmarks are detected, prompt the user to wait.
            setInstruction(
              data.landmarks_detected
                ? 'Hand erkannt. Warte auf die Bedingungen...'
                : 'Bitte platziere deine Hand im Kamerarahmen.',
            );
            break;
          case 'timer':
            // Display a countdown until the photo is captured
            setInstruction(`Foto wird in ${data.time} Sekunden aufgenommen...`);
            break;
          case 'taking_images':
            // Notify the user that image capture is in progress
            setInstruction('Bild wird aufgenommen...');
            break;
          case 'success':
            // Upon successful capture, update the image state and navigate to the post-capture view
            setInstruction('Bild erfolgreich aufgenommen!');
            updateCapturedImage(data.image!);
            setTimeout(() => navigate('/image-post-capture'), 1000);
            break;
          case 'error':
            // Display any error messages received from the backend
            setInstruction(`Fehler: ${data.message}`);
            break;
          default:
            // Fallback instruction if the flow is unrecognized
            setInstruction('Warte auf weitere Anweisungen...');
        }
      } catch {
        // If an error occurs while processing the backend response, notify the user
        setInstruction('Fehler beim Verarbeiten der Server-Antwort.');
      }
    };

    // Handle WebSocket connection closure
    ws.onclose = () => {
      console.log('WebSocket-Verbindung geschlossen');
      // Stop the video stream
      if (currentVideoRef?.srcObject) {
        const tracks = (currentVideoRef.srcObject as MediaStream).getTracks();
        tracks.forEach((track) => track.stop());
      }
    };

    // Cleanup function executed when the component unmounts
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
    <div style={{ margin: '2em 1.5em' }}>
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
    </div>
  );
}
