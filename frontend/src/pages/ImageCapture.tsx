import { Box, Typography } from '@mui/material';
import { styled } from '@mui/material/styles';
import StyledTitle from '@/styles/StyledTitle';
import NavButton from '@/components/NavButton';

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
`;

const StyledText = styled(Typography)`
  color: black;
  font-size: 1.6rem;
`;

const ImageCapture = () => {
  return (
    <Container>
      <VideoWrapper>
        <Video autoPlay playsInline />
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
        <InstructionBox />
        <NavButton RouteTo="/image-post-capture">Weiter</NavButton>
      </InfoSection>
    </Container>
  );
};

export default ImageCapture;
