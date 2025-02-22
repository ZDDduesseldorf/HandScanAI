//external imports
import React, { useState } from 'react';
import { TextField, MenuItem, Grid2 } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { useMutation } from '@apollo/client';

//internal imports
import { useAppStore } from '@/store/appStore';
import { UPDATE_SCAN_ENTRY } from '@/services/mutations';

//component imports
import Header from '@/components/custom/Header';
import Secondary from '@/components/headings/Secondary';
import WithMargins from '@/components/layout/WithMargins';
import Justified from '@/components/text/Justified';
import NarrowFixedBottomRight from '@/components/buttons/NarrowFixedBottomRight';
import NarrowFixedBottomLeft from '@/components/buttons/NarrowFixedBottomLeft';
import WithText from '@/components/cards/WithText';

/**
 * The second results page offers the option of entering the actual data for age
 * and gender. The data entered is simply validated and then sent to the backend.
 * So far, only male and female can be specified for gender, as HandScan AI has
 * not yet been trained for different genders.
 *
 * @returns Page showing input field to input actual data
 */
export default function Result_2() {
  /**
   * Method for changing the location
   * @see https://reactrouter.com/6.29.0/hooks/use-navigate
   */
  const navigate = useNavigate();

  /**
   * A list that stores the genders that are available for selection in the select menu.
   */
  const genders = [
    { value: '0', label: 'weiblich' },
    { value: '1', label: 'männlich' },
  ];

  const [
    /**
     * User input of their actual age that is stored in React state.
     */
    ageInput,
    /**
     * Saves the actual age in React state.
     */
    setAgeInput,
  ] = useState('');

  const [
    /**
     * User input of their actual gender that is stored in React state.
     */
    genderInput,
    /**
     * Saves the actual gender in React state.
     */
    setGenderInput,
  ] = useState('');

  /**
   * The id of the personal result of the scan stored in the React app store.
   */
  const scanId = useAppStore((state) => state.scanResult?.id);

  const [
    /**
     * Mutation to update the saved scan data
     * @see https://www.apollographql.com/docs/react/data/mutations
     */
    updateScanEntry,
  ] = useMutation(UPDATE_SCAN_ENTRY);

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
   * Checks whether a given string or number is numeric, i.e. consists only of
   * numbers.
   *
   * @param value string or number to be checked
   * @returns True, if the given string or number is numeric
   */
  function isNumeric(value?: string | number): boolean {
    return value != null && value !== '' && !isNaN(Number(value.toString()));
  }

  /**
   * Handels all actions that take place when the user leaves the page. If there is
   * input data, it is minimally validated and sent to the backend if the validation
   * is passed.
   * If the data is not complete or does not pass validation, the page simply
   * navigates to the next without sending anything to the backend.
   */
  function handleSubmit() {
    //check if the inputs are valid
    if (ageInput && genderInput && isNumeric(ageInput)) {
      //send to backend and navigate
      updateScanEntry({
        variables: {
          id: scanId,
          input: {
            realAge: parseInt(ageInput, 10),
            realGender: parseInt(genderInput, 10),
            confirmed: true,
          },
        },
      })
        .then(() => {
          void navigate('/explanation');
        })
        .catch((e) => console.error(e));
    } else {
      //just navigate
      void navigate('/explanation');
    }
  }

  return (
    <WithMargins mx="2em" my="1.5em">
      <Header title="Ergebnis" />
      <Secondary>KI kann Fehler machen</Secondary>
      <Justified>
        Auch wenn die KI leistungsstark ist, können Fehler auftreten. Überprüfe
        das Ergebnis, um sicherzugehen, dass es korrekt ist.
      </Justified>
      <Grid2 container spacing={8}>
        <Grid2 size="grow">
          <WithText title="Dein Alter">
            <p>
              Wahrscheinlich bist du {Math.round(scanResult.classifiedAge)}{' '}
              Jahre alt. <br />
              Na, haben wir dein Alter richtig erraten? Wir hoffen, wir haben
              dir geschmeichelt! <br />
              Teile uns dein echtes Alter mit - das hilft uns, HandScan AI zu
              verbessern! <br />
            </p>
            <TextField
              id="ageInput"
              value={ageInput}
              label="Alter"
              variant="outlined"
              fullWidth
              onChange={(event: React.ChangeEvent<HTMLInputElement>) => {
                setAgeInput(event.target.value);
              }}
            />
          </WithText>
        </Grid2>
        <Grid2 size="grow">
          <WithText title="Dein Geschlecht">
            <p>
              Wahrscheinlich bist du{' '}
              {scanResult.classifiedGender == 0 ? 'weiblich' : 'männlich'}.{' '}
              <br />
              Und was ist mit deinem Geschlecht? Stimmt die Vorhersage? <br />
              Teile uns dein Geschlecht mit - das hilft uns, HandScan AI zu
              verbessern! <br />
            </p>
            <TextField
              id="genderInput"
              select
              value={genderInput}
              label="Geschlecht"
              variant="outlined"
              fullWidth
              onChange={(event: React.ChangeEvent<HTMLInputElement>) => {
                setGenderInput(event.target.value);
              }}
            >
              {genders.map((option) => (
                <MenuItem key={option.value} value={option.value}>
                  {option.label}
                </MenuItem>
              ))}
            </TextField>
          </WithText>
        </Grid2>
      </Grid2>
      <NarrowFixedBottomLeft onClick={() => void navigate(-1)}>
        Zurück
      </NarrowFixedBottomLeft>
      <NarrowFixedBottomRight onClick={handleSubmit}>
        Weiter
      </NarrowFixedBottomRight>
    </WithMargins>
  );
}
