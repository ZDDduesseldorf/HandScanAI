import { Box, Typography, Button } from '@mui/material';
import { styled } from '@mui/material/styles';
import StyledTitle from '@/styles/StyledTitle';
import { useNavigate } from 'react-router-dom';
import { useAppStore } from '@/store/appStore';

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
`;

const ImagePostCapture = () => {
  const navigate = useNavigate();
  const capturedImage = useAppStore((state) => state.capturedImage);

  return (
    <Container>
      <StyledTitle>Wir haben ein Foto für dich und HandScanAI!</StyledTitle>
      <StyledText>
        Das Foto wird zu unserem Datensatz hinzugefügt, der mit jeder neuen
        Aufnahme wächst.
      </StyledText>
      <StyledText>
        Warum ist das so wichtig? Künstliche Intelligenz wird durch Daten
        trainiert. Je mehr Daten vorhanden sind, desto besser kann die KI Muster
        erkennen, Zusammenhänge verstehen und präzisere Vorhersagen treffen.
        Dein Foto trägt also dazu bei, dass HandScan AI nicht nur intelligenter,
        sondern auch vielfältiger und gerechter wird – denn ein breiter
        Datensatz hilft, Vorurteile (Bias) zu reduzieren.
      </StyledText>
      <ImagePlaceholder>
        {capturedImage ? (
          <img src={capturedImage} alt="Captured" style={{ maxWidth: '100%' }} />
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
