import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { styled } from '@mui/material/styles';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import { useMutation } from '@apollo/client';
import { CREATE_SCAN_ENTRY } from '@/services/mutations';
import { CreateScanEntryModelData } from '@/services/graphqlTypes';
import { useAppStore } from '@/store/appStore';
import { Alert, Snackbar } from '@mui/material';
import NavButton from '@/components/NavButton';

const Container = styled(Box)`
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
  width: 100vw;
  background-color: #ffffff;
`;

export const Logo = styled('img')`
  width: clamp(200px, 35%, 450px);
  margin-bottom: 1rem;
`;

export const Title = styled(Typography)`
  font-family: 'Delius Unicase', cursive;
  font-weight: 400;
  color: #1a3ab8;
  margin: 0 0 0.625rem;
  text-align: center;
  font-size: clamp(1.75rem, 4vw, 3.25rem);
`;

const Subtitle = styled(Typography)`
  font-family: 'Poppins', sans-serif;
  color: #1a3ab8;
  margin: 0 0 1.875rem;
  text-align: center;
  font-size: clamp(1rem, 2vw, 1.5rem);
`;

const StartButton = styled(Button)`
  background-color: #1a3ab8;
  color: #ffffff;
  font-family: 'Delius Unicase', cursive;
  text-transform: none;
  font-weight: bold;
  padding: clamp(0.75rem, 2vw, 1.25rem) clamp(1.5rem, 4vw, 2.5rem);
  border-radius: 1rem;
  font-size: clamp(0.875rem, 1.75vw, 1.25rem);
  width: clamp(10rem, 20vw, 18rem);
  border: none;
  transition: background-color 0.3s;

  &:hover {
    background-color: #516fe6;
  }
`;

const Home: React.FC = () => {
  const navigate = useNavigate();
  const [createScanEntry] =
    useMutation<CreateScanEntryModelData>(CREATE_SCAN_ENTRY);
  const setScanEntry = useAppStore((state) => state.setScanEntry);

  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const handleStartClick = async () => {
    try {
      const { data } = await createScanEntry();

      if (data?.createScanEntryModel) {
        setScanEntry(data.createScanEntryModel);
        console.log('Scan entry created:', data.createScanEntryModel);
        navigate('/privacy-notice');
      }
    } catch (error) {
      console.error('Error creating scan entry:', error);
      setErrorMessage(
        'Unable to open a session. The backend might be unavailable.',
      );
    }
  };

  const handleCloseSnackbar = () => {
    setErrorMessage(null);
  };

  return (
    <Container>
      <Logo src="/logo.png" alt="Hand Scan AI Logo" />
      <Title variant="h1">Hand Scan AI</Title>
      <Subtitle variant="h2">Scan it. Know it.</Subtitle>
      <StartButton onClick={() => void handleStartClick()}>Start</StartButton>
      {errorMessage && (
        <Snackbar
          open={!!errorMessage}
          autoHideDuration={6000}
          onClose={handleCloseSnackbar}
        >
          <Alert severity="error" onClose={handleCloseSnackbar}>
            {errorMessage}
          </Alert>
        </Snackbar>
      )}
      <NavButton RouteTo="/explanation">Debug Explanation</NavButton>
    </Container>
  );
};

export default Home;
