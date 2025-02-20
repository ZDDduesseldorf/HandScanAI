import { styled } from '@mui/material/styles';
import Box from '@mui/material/Box';
import Stepper from '@mui/material/Stepper'; // Stepper component for creating progress indicators
import Step from '@mui/material/Step'; // Represents an individual step in the Stepper
import StepLabel from '@mui/material/StepLabel'; // Label for each step in the Stepper

/**
 * Defines the typescript types of the parameters
 */
interface Props {
  pageNumber: number;
}

/**
 * Provides a stepper component that shows the progress of the page. The steps
 * already completed are ticked off and the current position is displayed.
 *
 * @param pageNumber The current page number
 * @returns Stepper component with the current position shown
 */
export default function FooterStepper({ pageNumber }: Props) {
  /**
   * The different steps of HandScan AI
   */
  const steps = ['Info', 'Bildaufnahme', 'Berechnung', 'Ergebnis', 'Erklärung'];

  /**
   * Styling for the mui <div> element that positions the stepper in the footer
   * area and provides a standardized style for the fonts inside of it.
   */
  const FooterContainer = styled(Box)`
    width: 100%;
    position: fixed;
    bottom: 0;
    margin-bottom: 15px;
    font-family: 'Delius Unicase', serif;
    font-weight: 400;
    font-style: normal;
    color: var(--primary);
  `;

  /**
   * Overrides the styling of mui's labels for the stepper with custom colors
   * and font families.
   */
  const StyledStepLabel = styled(StepLabel)(() => ({
    //overwrites label currently active
    '& .MuiStepLabel-label.Mui-active': {
      color: '#0f3eb5', // changes the font color
    },
    '& .MuiStepLabel-label': {
      //covers all Labels if not overwritten
      color: 'white', // changes the font color
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

      borderTopWidth: '20px', // Set the thickness of the horizontal line
    },
  }));
  return (
    <FooterContainer>
      {/* pageNumber sets which Stepper circle we are currently at  */}
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
