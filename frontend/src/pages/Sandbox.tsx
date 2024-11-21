import { useEffect, useRef, useState } from 'react';

interface ServerMessage {
  flow?: string;
  landmarks_detected?: boolean;
  spread_check?: boolean;
  [key: string]: unknown;
}

const Sandbox = () => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const wsRef = useRef<WebSocket | null>(null);
  const [resolution, setResolution] = useState<{
    width: number;
    height: number;
  }>();
  const [serverMessage, setServerMessage] = useState<
    ServerMessage | undefined
  >();

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
              setResolution({ width: videoWidth, height: videoHeight });

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
        setServerMessage(data);
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
  }, []);

  return (
    <div>
      <h1>Sandbox</h1>
      {resolution && (
        <p>
          Resolution: {resolution.width}x{resolution.height}
        </p>
      )}
      <div>
        <p>Server Response: {JSON.stringify(serverMessage)}</p>
      </div>
      <video ref={videoRef} style={{ maxWidth: '100%' }} autoPlay />
    </div>
  );
};

export default Sandbox;
