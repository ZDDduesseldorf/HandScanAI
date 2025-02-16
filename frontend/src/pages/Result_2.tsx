import React, { useState } from 'react';
import { TextField, MenuItem, Grid2 } from '@mui/material';
import { useNavigate } from 'react-router-dom';

import Header from '@/components/custom/Header';
import Secondary from '@/components/headings/Secondary';
import WithMargins from '@/components/layout/WithMargins';
import Justified from '@/components/text/Justified';
import NarrowBottomSticky from '@/components/buttons/NarrowBottomFixed';
import WithText from '@/components/cards/WithText';

// Vom Backend gebraucht:
// Geschlecht Guess
// Alter Guess

// ans Backend schicken:
// actual age
// actual gender

const genderGuess = 'weiblich';
const ageGuess = 26;

// Optionally, you can keep the GraphQL mutation if needed
// const CORRECT_HANDDATA = gql`
//   mutation MyMutation($id: ID!, $input: ScanEntryInput!) {
//     updateScanEntryModel(id: $id, input: $input) {
//       id
//     }
//   }
// `;

export default function Result_2() {
  const navigate = useNavigate();

  const genders = [
    {
      value: '0',
      label: 'männlich',
    },
    {
      value: '1',
      label: 'weiblich',
    },
  ];

  const [ageInput, setAgeInput] = useState('');
  const [genderInput, setGenderInput] = useState('');
  // const scanId = '5274cc1e-6413-4653-b14f-a4fcba138c99';

  // The updateScanEntry mutation can be used when implemented
  // const [updateScanEntry, { error, data }] = useMutation(CORRECT_HANDDATA);

  // handleSubmit function can be implemented later
  // const handleSubmit = () => {
  //   updateScanEntry({
  //     variables: {
  //       id: scanId,
  //       input: {
  //         realAge: parseInt(ageInput, 10),
  //         realGender: parseInt(genderInput, 10),
  //       },
  //     },
  //   }).then(() => alert('Daten wurden aktualisiert!'));
  // };

  return (
    <>
      <Header title="Ergebnis" />
      <WithMargins mx="2em" my="1.5em">
        <Secondary>KI kann Fehler machen</Secondary>
        <Justified>
          Auch wenn die KI leistungsstark ist, können Fehler auftreten.
          Überprüfe das Ergebnis, um sicherzugehen, dass es korrekt ist.
        </Justified>
        <Grid2 container spacing={2}>
          <Grid2 size={6}>
            <WithText title="Dein Alter">
              <p>
                Wahrscheinlich bist du {ageGuess} Jahre alt. <br />
                Na, haben wir dein Alter richtig erraten? Wir hoffen, wir haben dir
                geschmeichelt! <br />
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
          <Grid2 size={6}>
            <WithText title="Dein Geschlecht">
              <p>
                Wahrscheinlich bist du {genderGuess}. <br />
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
        <NarrowBottomSticky onClick={() => navigate('/submission-complete')}>
          Weiter
        </NarrowBottomSticky>
      </WithMargins>
    </>
  );
}
