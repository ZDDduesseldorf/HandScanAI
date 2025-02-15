import Slider from '@mui/material/Slider';
import { useNavigate } from 'react-router-dom';

import WithMargins from '@/components/layout/WithMargins';
import Header from '@/components/custom/Header';
import Secondary from '@/components/headings/Secondary';
import Tertiary from '@/components/headings/Tertiary';
import Justified from '@/components/text/Justified';
import NarrowBottomSticky from '@/components/buttons/NarrowBottomFixed';

// Vom Backend gebraucht:
// Geschlecht Guess
// (Alter Range Guess)
// Alter Guess
// Alter Accuracy (Wie sicher ist sich KI?)
// Geschlecht Accuracy (Wie sicher ist sich KI?)

const genderGuess = 0;
const ageGuess = 26;
const min_age = 20;
const max_age = 26;
const age_confidence = 97;
const gender_confidence = 95;

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

export default function Result_1 () {
  const navigate = useNavigate();

  return (
    <>
      <Header title="Ergebnis" />
      <WithMargins mx="2em" my="1.5em">
        <Secondary>
          Du bist {genderGuess ? 'weiblich' : 'männlich'} und {ageGuess} Jahre alt
        </Secondary>
        <Tertiary>Dein Alter</Tertiary>
        <Justified>
          HandScan AI ist sich zu {age_confidence}% sicher, dass du zwischen{' '}
          {min_age} und {max_age} Jahre alt bist
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
          HandScan AI ist sich zu {gender_confidence}% sicher, dass du{' '}
          {genderGuess ? 'weiblich' : 'männlich'} bist
        </Justified>
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
        <NarrowBottomSticky onClick={() => navigate("/result-2")}>Weiter</NarrowBottomSticky>
      </WithMargins>
    </>
  );
};
