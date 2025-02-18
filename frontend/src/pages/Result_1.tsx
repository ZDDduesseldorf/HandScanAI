import Slider from '@mui/material/Slider';
import { useNavigate } from 'react-router-dom';
import { useAppStore } from '@/store/appStore';

import WithMargins from '@/components/layout/WithMargins';
import Header from '@/components/custom/Header';
import Secondary from '@/components/headings/Secondary';
import Tertiary from '@/components/headings/Tertiary';
import Justified from '@/components/text/Justified';
import NarrowBottomSticky from '@/components/buttons/NarrowFixedBottomRight';

// Vom Backend gebraucht:
// Geschlecht Guess
// (Alter Range Guess)
// Alter Guess
// Alter Accuracy (Wie sicher ist sich KI?)
// Geschlecht Accuracy (Wie sicher ist sich KI?)

//const genderGuess = 0;
//const ageGuess = 26;
//const min_age = 20;
//const max_age = 26;
// const age_confidence = 97;
//const gender_confidence = 95;

export default function Result_1() {
  const navigate = useNavigate();
  const scanResult = useAppStore((state) => state.scanResult);
  
  if (!scanResult) {
    return (
      <p>Keine Daten vorhanden, Bitte gehen sie zur vorherigen Seite zurück</p>
    );
  }

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

  // Override globals with values from the backend scanResult
  const genderGuess = scanResult.classifiedAge;
  const ageGuess = scanResult.classifiedAge;
  const min_age = scanResult.minAge;
  const max_age = scanResult.maxAge;
  //const age_confidence = scanResult.confidenceAge;
  const gender_confidence = scanResult.confidenceGender;

  return (
    <>
      <Header title="Ergebnis" />
      <WithMargins mx="2em" my="1.5em">
        <Secondary>
          Du bist {genderGuess == 1 ? 'männlich' : 'weiblich'} und {Math.round(ageGuess)} Jahre
          alt
        </Secondary>
        <Tertiary>Dein Alter</Tertiary>
        <Justified>
          HandScan AI denkt, dass du wahrscheinlich {Math.round(ageGuess)} Jahre alt bist, 
          denn 90% von ähnlichen Händen waren ebenfalls zwischen {Math.round(min_age)} und {Math.round(max_age)} Jahre alt.
        </Justified>
        <Slider
          disabled
          defaultValue={ageGuess}
          aria-label="Age guess"
          track={false}
          marks={age_marks}
          min={15}
          max={85}
        />
        <Tertiary>Dein Geschlecht</Tertiary>
        <Justified>
          HandScan AI ist sich zu {Math.round(gender_confidence*100)}% sicher, dass du{' '}
          {genderGuess == 1 ? 'männlich' : 'weiblich'} bist
        </Justified>
        <Slider
          disabled
          defaultValue={gender_confidence*100}
          valueLabelDisplay="auto"
          aria-label="Gender guess"
          track={false}
          marks={[
            { value: 0, label: '0%' },
            { value: 50, label: '50%'},
            { value: 100, label: '100%' },
          ]}
          min={0}
          max={100}
        />
        <NarrowBottomSticky onClick={() => navigate('/result-2')}>
          Weiter
        </NarrowBottomSticky>
      </WithMargins>
    </>
  );
}
