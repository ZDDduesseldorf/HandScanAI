import { styled } from '@mui/material/styles';
import Box from '@mui/material/Box';
import Stepper from '@mui/material/Stepper';
import Step from '@mui/material/Step';
import StepLabel from '@mui/material/StepLabel';

const steps = ['Info', 'Bildaufnahme', 'Berechnung', 'Ergebnis', 'Abschluss'];

interface Props {
  pageNumber: number;
}

const FooterContainer = styled(Box)`
  width: 100%;
  position: fixed;
  bottom: 0;
  margin-bottom: 15px;
  font-family: 'Delius Unicase', serif;
  font-weight: 400;
  font-style: normal;
  color: #0f3eb5;
`;

const StyledStepLabel = styled(StepLabel)`
  color: #0f3eb5;
`;

export default function FooterStepper({ pageNumber }: Props) {
  return (
    <FooterContainer>
      <Stepper activeStep={pageNumber} alternativeLabel>
        {steps.map((label) => (
          <Step key={label}>
            <StyledStepLabel>{label}</StyledStepLabel>
          </Step>
        ))}
      </Stepper>
    </FooterContainer>
  );
}
