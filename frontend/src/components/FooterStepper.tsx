import { styled } from '@mui/material/styles';
import Box from '@mui/material/Box';
import Stepper from '@mui/material/Stepper'; // Stepper component for creating progress indicators
import Step from '@mui/material/Step'; // Represents an individual step in the Stepper
import StepLabel from '@mui/material/StepLabel'; // Label for each step in the Stepper

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

const StyledStepLabel = styled(StepLabel)(() => ({
  //overwrites label currently active
  '& .MuiStepLabel-label.Mui-active': {
    color: '#0f3eb5', // changes the font color
  },
  '& .MuiStepLabel-label': {
    //covers all Labels if not overwritten
    color: '#000000', // changes the font color
    fontFamily: 'Delius Unicase, serif',
  },
  '& .MuiStepLabel-label.Mui-completed': {
    //overwrites labels we have already passed
    color: '#0f3eb5', // changes the font color
  },
  //Dealing with Icons
  // the icons with a checkered sign, dont use circle + text but a path pointing to an svg!!!
  '& .MuiStepIcon-root.Mui-active': {
    color: '#0f3eb5', // changes the circle color
  },
  '& .MuiStepIcon-root.Mui-completed': {
    color: '#0f3eb5', // changes the circle color
    //height: '3em',
  },
  '& .MuiStepIcon-text': {
    // work around to hide the numbers in the circles, color transparency set to 0
    fill: '#00000000',
  },

  //Horizontal Line Between Circles
  '& .MuiStepConnector-line': {
    //not inside Step Label but inside of the step class!!!
    borderTopColor: '#0f3eb5', // Set the line color
    borderColor: '#0f3eb5', // Set the line color

    // fill: '#00000000',
    // lineHeight: '5em',
    // bordertopwidth: '5px',
    borderTopWidth: '20px', // Set the thickness of the horizontal line
  },
}));

export default function FooterStepper({ pageNumber }: Props) {
  return (
    <FooterContainer>
      {/* pageNumber sets which Stepper circle we are currently at  */}
      <Stepper activeStep={pageNumber} alternativeLabel>
        {steps.map((label) => (
          <Step key={label}>
            <StyledStepLabel
            // sx={{ '& .MuiStepLabel-IconContainer': { color: '#0f3eb5' } }}
            >
              {label}
            </StyledStepLabel>
          </Step>
        ))}
      </Stepper>
    </FooterContainer>
  );
}
