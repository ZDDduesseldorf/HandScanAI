import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useMutation } from '@apollo/client';
import { Alert, Snackbar } from '@mui/material';
import { CREATE_SCAN_ENTRY } from '@/services/mutations';
import { CreateScanEntryModelData } from '@/services/graphqlTypes';
import { useAppStore } from '@/store/appStore';

import Centered from '@/components/layout/CenteredFullWidth';
import LogoXL from '@/components/custom/LogoXL';
import Title from '@/components/headings/Title';
import Subtitle from '@/components/headings/Subtitle';
import WideButton from '@/components/buttons/Wide';

export default function Home() {
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
    <Centered>
      <LogoXL src="/logos/logo.png" alt="Hand Scan AI Logo" />
      <Title>Hand Scan AI</Title>
      <Subtitle>Scan it. Know it.</Subtitle>
      <WideButton onClick={() => void handleStartClick()}>Start</WideButton>
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
    </Centered>
  );
}
