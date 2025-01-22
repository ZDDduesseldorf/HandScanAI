import { Box, Typography } from '@mui/material';
import { styled } from '@mui/material/styles';
import StyledTitle from '@/styles/StyledTitle';
import NavButton from '@/components/NavButton';
import { useEffect, useRef, useState } from 'react';
import { useAppStore } from '@/store/appStore';
import { useNavigate } from 'react-router-dom';

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
  margin: 20px auto;
  padding: 20px;
  background-color: #f0f0f0;
  border-radius: 12px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
`;

const VideoWrapper = styled(Box)`
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  width: 30%;
  height: 60vh;
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

const StyledText = styled(Typography)`
  color: black;
  font-size: 1.6rem;
`;

const ImageCapture = () => {
  const navigate = useNavigate();
  const scanEntry = useAppStore((state) => state.scanEntry);
  const updateCapturedImage = useAppStore((state) => state.setCapturedImage);
  const videoRef = useRef<HTMLVideoElement>(null);
  const wsRef = useRef<WebSocket | null>(null);
  const [instruction, setInstruction] = useState('Preparing camera...');
  const [resolution, setResolution] = useState<{
    width: number;
    height: number;
  }>();
  const [serverMessage, setServerMessage] = useState<
    ServerMessage | undefined
  >();

  useEffect(() => {
    if (!scanEntry?.id) {
      console.error('Invalid scan entry ID.');
      alert('Scan entry ID is missing or invalid. Please restart the process.');
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
              console.error('Error playing video:', error);
            });

            currentVideoRef.onloadedmetadata = () => {
              const videoWidth = currentVideoRef.videoWidth;
              const videoHeight = currentVideoRef.videoHeight;
              canvas.width = videoWidth;
              canvas.height = videoHeight;
              setResolution({ width: videoWidth, height: videoHeight });

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
              }, 100);
            };
          }
        })
        .catch((error) => {
          setInstruction('Error accessing camera.');
          console.error('Error accessing camera:', error);
        });
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data as string) as ServerMessage;
        setServerMessage(data);

        switch (data.flow) {
          case 'validation':
            setInstruction(
              data.landmarks_detected
                ? 'Hand detected. Waiting for conditions...'
                : 'Place your hand in the camera frame.',
            );
            break;
          case 'timer':
            setInstruction(`Taking picture in ${data.time} seconds...`);
            break;
          case 'taking_images':
            setInstruction('Capturing image...');
            break;
          case 'success':
            setInstruction('Image captured successfully!');
            updateCapturedImage(data.image!);
            setTimeout(() => navigate('/image-post-capture'), 1000);
            break;
          case 'error':
            setInstruction(`Error: ${data.message}`);
            break;
          default:
            setInstruction('Awaiting further instructions...');
        }
      } catch {
        setInstruction('Error parsing server response.');
      }
    };

    ws.onclose = () => {
      console.log('WebSocket connection closed');
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
    <Container>
      <VideoWrapper>
        <Video ref={videoRef} autoPlay playsInline />
      </VideoWrapper>
      <InfoSection>
        <StyledTitle>Bildaufnahme</StyledTitle>
        <StyledText>
          HandScan AI nimmt automatisch Bilder deiner Hand auf. Sobald die
          Kamera eine Hand erkennt, wird der Countdown gestartet.
        </StyledText>
        <StyledText sx={{ mt: 1 }}>
          👉 Bitte lege deine Hand mit der Handfläche nach unten in die Fotobox.
        </StyledText>
        <StyledText sx={{ mt: 1 }}>
          👉 Es ist egal, ob du die rechte oder linke Hand nimmst.
        </StyledText>
        <InstructionBox>
          <Typography>{instruction}</Typography>
        </InstructionBox>
        <NavButton RouteTo="/image-post-capture">Weiter</NavButton>
      </InfoSection>
    </Container>
  );
};

export default ImageCapture;
