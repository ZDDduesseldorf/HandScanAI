//import * as React from 'react';
import Box from '@mui/material/Box';
import Stepper from '@mui/material/Stepper';
import Step from '@mui/material/Step';
import StepLabel from '@mui/material/StepLabel';

const steps = ['Info', 'Bildaufnahme', 'Berechnung', 'Ergebnis'];

import './Stepper.css';

//still needs to be customized

interface Props {
  pageNumber: number;
}

export default function HorizStepper({ pageNumber }: Props) {
  const footerStyle: React.CSSProperties = {
    position: 'fixed',
    bottom: '0',
    width: '100%',
    marginBottom: '15px',
  };

  return (
    <div style={footerStyle}>
      <Box sx={{ width: '100%' }}>
        <Stepper activeStep={pageNumber} alternativeLabel>
          {steps.map((label) => (
            <Step key={label}>
              <StepLabel>{label}</StepLabel>
            </Step>
          ))}
        </Stepper>
      </Box>
    </div>
  );
}
