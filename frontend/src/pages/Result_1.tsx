//external imports
import { useNavigate } from 'react-router-dom';
import Slider from '@mui/material/Slider';

//internal imports
import { useAppStore } from '@/store/appStore';

//component imports
import WithMargins from '@/components/layout/WithMargins';
import Header from '@/components/custom/Header';
import Secondary from '@/components/headings/Secondary';
import Tertiary from '@/components/headings/Tertiary';
import Justified from '@/components/text/Justified';
import NarrowBottomSticky from '@/components/buttons/NarrowFixedBottomRight';

/**
 * The first results page shows the classified results. The data is displayed
 * as text and also as a slider for visualization.
 *
 * @returns Page showing the classified results
 */
export default function Result_1() {
  /**
   * Method for changing the location
   * @see https://reactrouter.com/6.29.0/hooks/use-navigate
   */
  const navigate = useNavigate();

  /**
   * The personal result of the scan stored in the React app store.
   */
  const scanResult = useAppStore((state) => state.scanResult);

  if (!scanResult) {
    return (
      <p>Keine Daten vorhanden, Bitte gehen sie zur vorherigen Seite zurück</p>
    );
  }

  /**
   * A list with the markers for the age that are below the slider. value is the
   * value of the variable for the age and label is the corresponding label.
   */
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

  /**
   * The classified gender, which is retrieved from the React store.
   */
  const genderGuess = scanResult.classifiedAge;

  /**
   * The classified age, which is retrieved from the React store.
   */
  const ageGuess = scanResult.classifiedAge;

  /**
   * The minimum age that is retrieved from the React Store.
   */
  const min_age = scanResult.minAge;

  /**
   * The maximum age that is retrieved from the React Store.
   */
  const max_age = scanResult.maxAge;

  /**
   * The confidence (in percent) of the classifier, which indicates how likely the
   * result is to be correct.
   */
  const gender_confidence = scanResult.confidenceGender;

  return (
    <WithMargins mx="2em" my="1.5em">
      <Header title="Ergebnis" />
      <Secondary>
        Du bist {genderGuess == 1 ? 'männlich' : 'weiblich'} und{' '}
        {Math.round(ageGuess)} Jahre alt
      </Secondary>
      <div style={{ marginTop: '4em' }}>
        <Tertiary>Dein Alter</Tertiary>
        <Justified>
          HandScan AI denkt, dass du wahrscheinlich {Math.round(ageGuess)} Jahre
          alt bist, denn 90% von ähnlichen Händen waren ebenfalls zwischen{' '}
          {Math.round(min_age)} und {Math.round(max_age)} Jahre alt.
        </Justified>
        <Slider
          disabled
          defaultValue={ageGuess}
          aria-label="Age guess"
          track={false}
          marks={age_marks}
          min={15}
          max={85}
          style={{
            width: '70vw',
            margin: '1em 1.5em',
            color: 'var(--primary)',
          }}
        />
      </div>
      <div style={{ marginTop: '4em' }}>
        <Tertiary>Dein Geschlecht</Tertiary>
        <Justified>
          HandScan AI ist sich zu {Math.round(gender_confidence * 100)}% sicher,
          dass du {genderGuess == 1 ? 'männlich' : 'weiblich'} bist.
        </Justified>
        <Slider
          disabled
          defaultValue={gender_confidence * 100}
          valueLabelDisplay="auto"
          aria-label="Gender guess"
          track={false}
          marks={[
            { value: 0, label: '0%' },
            { value: 25, label: '25%' },
            { value: 50, label: '50%' },
            { value: 75, label: '75%' },
            { value: 100, label: '100%' },
          ]}
          min={0}
          max={100}
          style={{
            width: '70vw',
            margin: '1em 1.5em',
            color: 'var(--primary)',
          }}
        />
      </div>
      <NarrowBottomSticky onClick={() => navigate('/result-2')}>
        Weiter
      </NarrowBottomSticky>
    </WithMargins>
  );
}
