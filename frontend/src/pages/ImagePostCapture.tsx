import { Box, Typography, Button } from '@mui/material';
import { styled } from '@mui/material/styles';
import StyledTitle from '@/styles/StyledTitle';
import { useEffect, useState } from 'react';
import { useAppStore } from '@/store/appStore';
import { useNavigate } from 'react-router-dom';

const Container = styled(Box)`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 80%;
  margin: 20px auto;
  padding: 20px;
  background-color: #f0f0f0;
  border-radius: 12px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
`;

const ButtonContainer = styled(Box)`
  display: flex;
  flex-direction: row;
  gap: 20px;
  margin-top: 20px;
  justify-content: center;
`;

const ImagePlaceholder = styled(Box)`
  width: 200px;
  height: 200px;
  border: 2px dashed #ccc;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 20px 0;
`;

const StyledButton = styled(Button)`
  background-color: #0033cc;
  color: white;
  font-size: 1.2rem;
  padding: 10px 20px;
  &:hover {
    background-color: #0022aa;
  }
`;

const OutlinedButton = styled(Button)`
  border: 2px solid #0033cc;
  color: #0033cc;
  font-size: 1.2rem;
  padding: 10px 20px;
  background-color: transparent;
  &:hover {
    background-color: rgba(0, 51, 204, 0.1);
  }
`;

const StyledText = styled(Typography)`
  color: black;
  font-size: 1.6rem;
  margin-top: 10px;
`;

const ImagePostCapture: React.FC = () => {
  const navigate = useNavigate();
  const capturedImage = useAppStore((state) => state.capturedImage);
  const [displayImage, setDisplayImage] = useState<string | null>(null);

  useEffect(() => {
    let objectURL: string | undefined;
    if (capturedImage) {
      fetch(capturedImage, { cache: 'no-store' })
        .then((res: Response) => res.blob())
        .then((blob: Blob) => {
          objectURL = URL.createObjectURL(blob);
          setDisplayImage(objectURL);
        })
        .catch((err: unknown) => {
          console.error('Error fetching image:', err);
        });
    }
    return () => {
      if (objectURL) {
        URL.revokeObjectURL(objectURL);
      }
    };
  }, [capturedImage]);

  return (
    <Container>
      <StyledTitle>Wir haben ein Foto für dich und HandScanAI!</StyledTitle>
      <StyledText>
        Das Foto wird zu unserem Datensatz hinzugefügt, der mit jeder neuen
        Aufnahme wächst.
      </StyledText>
      <StyledText>
        Warum ist das so wichtig? Künstliche Intelligenz wird durch Daten
        trainiert – je mehr Daten, desto besser!
      </StyledText>
      <ImagePlaceholder>
        {displayImage ? (
          <img
            src={displayImage}
            alt="Captured"
            style={{ maxWidth: '100%', borderRadius: '8px' }}
          />
        ) : (
          <Typography>Image placeholder</Typography>
        )}
      </ImagePlaceholder>
      <StyledText>
        Klicke auf „Analyse starten“, um herauszufinden, was HandScanAI über
        deine Hand verrät!
      </StyledText>
      <ButtonContainer>
        <StyledButton onClick={() => navigate('/processing')}>
          Analyse starten
        </StyledButton>
        <OutlinedButton onClick={() => navigate('/image-capture')}>
          Neu aufnehmen
        </OutlinedButton>
      </ButtonContainer>
    </Container>
  );
};

export default ImagePostCapture;
