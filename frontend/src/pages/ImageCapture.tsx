import { useEffect, useRef } from 'react';
import { Box } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { styled } from '@mui/material/styles';
import StyledTitle from '@/styles/StyledTitle';
import NavButton from '@/components/buttons/Navigation';

interface ServerMessage {
  flow?: string;
  landmarks_detected?: boolean;
  spread_check?: boolean;
  [key: string]: unknown;
}

const ScrollableBox = styled(Box)`
  margin: 20px 30px;
  overflow-y: auto;
  max-height: calc(100vh - 300px); /* Adjust based on your layout */
`;

const VideoWrapper = styled(Box)`
  display: flex;
  width: 100%;
`;

const Video = styled('video')`
  width: 40%;
  height: auto;
  margin: 0 auto;
  max-height: 50vh;
  border-radius: 8px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.25);
`;

const Bildaufnahme = () => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const wsRef = useRef<WebSocket | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const currentVideoRef = videoRef.current;
    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d');
    const ws = new WebSocket('ws://localhost:8000/ws/');
    wsRef.current = ws;

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

              setInterval(() => {
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
          console.error('Error accessing camera:', error);
        });
    };

    ws.onmessage = (event) => {
      try {
        const eventData = event.data as string;
        const data = JSON.parse(eventData) as ServerMessage;

        // Redirect if hand detection is successful
        if (data.landmarks_detected) {
          navigate('/berechnung');
        }
      } catch (error) {
        console.error('Error parsing JSON:', error);
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
      if (currentVideoRef?.srcObject) {
        const tracks = (currentVideoRef.srcObject as MediaStream).getTracks();
        tracks.forEach((track) => track.stop());
      }
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [navigate]);

  return (
    <ScrollableBox>
      <StyledTitle>Bildaufnahme</StyledTitle>
      <VideoWrapper>
        <Video ref={videoRef} autoPlay />
      </VideoWrapper>
      <NavButton RouteTo="/processing">Weiter</NavButton>
    </ScrollableBox>
  );
};

export default Bildaufnahme;
