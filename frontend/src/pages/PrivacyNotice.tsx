import React from 'react';
import { Typography, Button, Box, styled } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import StyledTitle from '@/styles/StyledTitle';
import NavButton from '@/components/buttons/Navigation';

const BoxLayout = styled(Box)`
  display: flex;
  flex-direction: column;
  gap: 24px;
  width: 90%; /* Expands while keeping margins */
  max-width: 1000px; /* Prevents it from being too narrow */
  margin: 0 auto;
`;

const ContentBox = styled(Box)(({ theme }) => ({
  borderRadius: theme.shape.borderRadius * 2.5,
  backgroundColor: '#f5f5f5', // Softer gray for better readability
  color: '#333', // Darker text for better contrast
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'flex-start',
  justifyContent: 'space-between',
  padding: theme.spacing(3),
  boxShadow: '0px 4px 10px rgba(0, 0, 0, 0.1)', // Slight shadow for depth
  width: '100%', // Ensures it takes up full space
  '&:hover': {
    backgroundColor: '#e8e8e8',
  },
}));

const BoxText = styled(Typography)`
  font-family: 'Poppins', sans-serif;
  margin-bottom: 1rem;
  text-align: justify;
  font-size: 0.95rem;
  line-height: 1.5;
`;

const SecondaryHeading = styled(Typography)`
  font-family: 'Delius Unicase', cursive;
  margin-bottom: 0.5rem;
  text-align: left;
  font-size: clamp(1.3rem, 2vw, 1.8rem);
  font-weight: bold;
`;

const AcceptContainer = styled(Box)`
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  margin-top: 10px;
`;

const ContinueButton = styled(Button)`
  font-size: 1.1rem;
  padding: 14px 80px;
  border-radius: 8px;
  background-color: #1976d2; // Primary color
  color: white;
  text-transform: none;
  font-weight: bold;
  &:hover {
    background-color: #1565c0;
  }
`;

const PrivacyNotice: React.FC = () => {
  const navigate = useNavigate();

  return (
    <Box>
      <BoxLayout>
        <StyledTitle>Bevor wir Beginnen</StyledTitle>
        <ContentBox>
          <SecondaryHeading>Daten statt Gebühren</SecondaryHeading>
          <BoxText>
            Wie bei vielen digitalen Diensten gilt auch hier: Statt eines
            klassischen Preises zahlen Sie mit etwas anderem – Ihren Daten. In
            unserer App sind es vor allem Ihre Interaktionen und die Bilder
            Ihrer Hand, die die KI verarbeitet und lernen lässt. Diese Daten
            sind der „Treibstoff“, der der KI hilft, intelligenter, präziser und
            anpassungsfähiger zu werden.
          </BoxText>
        </ContentBox>

        <ContentBox>
          <SecondaryHeading>Einwilligung zur Datennutzung</SecondaryHeading>
          <BoxText>
            Indem Sie unsere App nutzen, erklären Sie sich ausdrücklich damit
            einverstanden, dass Ihre Daten für die Verbesserung der KI-Modelle
            genutzt werden. Diese Daten werden anonymisiert und im Modell
            gespeichert. Unsere KI wird Open Source unter der MIT Lizenz von
            GitHub veröffentlicht, was bedeutet, dass die Daten weiterleben
            können.
          </BoxText>

          <BoxText>
            Mit Ihrer Zustimmung stimmen Sie der Verarbeitung und
            Veröffentlichung Ihrer anonymisierten Daten innerhalb dieses
            Open-Source-Modells zu. Weitere Informationen finden Sie hier:
            Datenschutzmerkblatt.
          </BoxText>

          <AcceptContainer>
            <BoxText>Ich akzeptiere die Datenverarbeitung.</BoxText>
            <ContinueButton onClick={() => navigate('/image-capture')}>
              Weiter
            </ContinueButton>
          </AcceptContainer>
        </ContentBox>
      </BoxLayout>
      <NavButton RouteTo="/image-capture">Weiter</NavButton>
    </Box>
  );
};

export default PrivacyNotice;
