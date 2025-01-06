import React from 'react';
import { Button, Typography, styled, Box } from '@mui/material';
import { useNavigate } from 'react-router-dom';

const CenteredInformationText = styled(Typography)`
  font-family: 'Delius Unicase', cursive;
  color: #1a3ab8;
  text-align: center;
  font-size: clamp(1rem, 2vw, 1.5rem);
  margin-bottom: 20px;
`;

const Processing: React.FC = () => {
  const navigate = useNavigate();

  return (
    <Box>
      <CenteredInformationText>
        Ungefähr 90% der Menschen sind Rechtshänder,
        <br />
        wobei die Handdominanz oft in der frühen Kindheit <br />
        festgelegt wird und teilweise genetisch beeinflusst
        <br /> ist.
      </CenteredInformationText>

      <Button
        variant="contained"
        color="primary"
        onClick={() => navigate('/results-age')}
        sx={{ marginTop: 2 }}
      >
        Weiter
      </Button>
    </Box>
  );
};

export default Processing;
