import { Typography, Button, styled, Box } from '@mui/material';
import Slider from '@mui/material/Slider';
import { useNavigate } from 'react-router-dom';
import { useAppStore } from '@/store/appStore';

const TertiaryHeading = styled(Typography)`
  font-family: 'Delius Unicase', cursive;
  margin: 0 0 0.5rem;
  text-align: left;
  font-size: clamp(1rem, 2vw, 1.5rem);
`;

const BodyLayout = styled(Box)`
  margin: 20px;
  margin-right: 30px;
  margin-left: 30px;
`;

const BoxText = styled(Typography)`
  font-family: 'Poppins', sans-serif;
  margin: 0 0 1 rem;
  text-align: justify;
  // font-size: clamp(1rem, 2vw, 1.5rem);
  font-size: 0.8rem;
`;

const SecondaryHeading = styled(Typography)`
  font-family: 'Delius Unicase', cursive;
  margin: 0 0 0.5rem;
  text-align: left;
  font-size: clamp(1rem, 2vw, 1.5rem);
`;

// Vom Backend gebraucht:
// Geschlecht Guess
// (Alter Range Guess)
// Alter Guess
// Alter Accuracy (Wie sicher ist sich KI?)
// Geschlecht Accuracy (Wie sicher ist sich KI?)

const age_marks: { label: string; value: number }[] = [
  { value: 15, label: '<15' },
  { value: 25, label: '25' },
  { value: 35, label: '35' },
  { value: 45, label: '45' },
  { value: 55, label: '55' },
  { value: 65, label: '65' },
  { value: 75, label: '75' },
  { value: 85, label: '85+' },
];

const Result_1: React.FC = () => {
  const navigate = useNavigate();
  const scanResult = useAppStore((state) => state.scanResult);

  if (!scanResult) {
    return (
      <p>Keine Daten vorhanden, Bitte gehen sie zur vorherigen Seite zurück</p>
    );
  }

  const genderGuess = scanResult.classifiedAge;
  const ageGuess = scanResult.classifiedAge;
  const min_age = scanResult.minAge;
  const max_age = scanResult.maxAge;
  const age_confidence = scanResult.confidenceAge;
  const gender_confidence = scanResult.confidenceGender;

  return (
    <BodyLayout>
      Ergebnis
      <SecondaryHeading>
        Du bist {genderGuess ? 'weiblich' : 'männlich'} und {ageGuess} Jahre alt
      </SecondaryHeading>
      <TertiaryHeading>Dein Alter</TertiaryHeading>
      <BoxText>
        HandScan AI ist sich zu {age_confidence}% sicher, dass du zwischen{' '}
        {min_age} und {max_age} Jahre alt bist
      </BoxText>
      <Slider
        disabled
        defaultValue={ageGuess}
        aria-label="Age guess"
        track={false}
        marks={age_marks}
        min={15}
        max={85}
      />
      <TertiaryHeading>Dein Geschlecht</TertiaryHeading>
      <BoxText>
        HandScan AI ist sich zu {gender_confidence}% sicher, dass du{' '}
        {genderGuess ? 'weiblich' : 'männlich'} bist
      </BoxText>
      <Slider
        disabled
        defaultValue={genderGuess}
        valueLabelDisplay="auto"
        aria-label="Gender guess"
        track={false}
        marks={[
          { value: 0, label: 'männlich' },
          { value: 1, label: 'weiblich' },
        ]}
        min={0}
        max={1}
      />
      <Button
        variant="contained"
        color="primary"
        onClick={() => navigate('/result-2')}
      >
        Weiter
      </Button>
    </BodyLayout>
  );
};

export default Result_1;
