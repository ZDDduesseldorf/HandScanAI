// import React from 'react';
import { Button } from '@mui/material';
import { Typography, TextField, MenuItem, Box, styled } from '@mui/material';
//import { useNavigate } from 'react-router-dom';
import React, { useState } from 'react';
import { gql, useMutation } from '@apollo/client';

// Vom Backend gebraucht:
// Geschlecht Guess
// Alter Guess

// ans Backend schicken:
// actual age
// actual gender

const genderGuess = 'weiblich';
const ageGuess = 26;

export const BoxForm = styled(Box)`
  display: flex;
  flex-direction: column;
  justify-content: space-between;

  gap: 20px; /* Optional: adds space between the two boxes */
}
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

// Define the GraphQL mutation
const CORRECT_HANDDATA = gql(`
  mutation MyMutation($id: ID!, $input: ScanEntryInput!) {
    updateScanEntryModel(id: $id, input: $input) {
      id
    }
  }
`);

// Use the mutation hook

const Result_2: React.FC = () => {
  //const navigate = useNavigate();

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
  const scanId = '5274cc1e-6413-4653-b14f-a4fcba138c99';

  // const [updateScanEntry, { error, data }] = useMutation(CORRECT_HANDDATA);

  //handle Submit will likely have to be implemented on the last page to finally
  // sign off on the data, before passing it to the backend!
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
    <BodyLayout>
      Ergebnis
      <SecondaryHeading>KI kann Fehler machen</SecondaryHeading>
      <BoxText>
        Auch wenn die KI leistungsstark ist, können Fehler auftreten. Überprüfe
        das Ergebnis, um sicherzugehen, dass es korrekt ist.
      </BoxText>
      <BoxForm>
        <SecondaryHeading>Dein Alter</SecondaryHeading>
        <BoxText>
          Wahrscheinlich bist du {ageGuess} Jahre alt. <br />
          Na, haben wir dein Alter richtig erraten? Wir hoffen, wir haben die
          geschmeichelt! <br />
          Teile uns dein echtes Alter mit - das hilft uns, HandScan AI zu
          verbessern! <br />
        </BoxText>
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
        <SecondaryHeading>Dein Geschlecht</SecondaryHeading>
        <BoxText>
          Wahrscheinlich bist du {genderGuess}. <br />
          Und was ist mit deinem Geschlecht? Stimmt die Vorhersage? <br />
          Teile uns dein Geschlecht mit - das hilft uns, HandScan AI zu
          verbessern! <br />
        </BoxText>
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
      </BoxForm>
      <Button
        variant="contained"
        color="primary"
        onClick={() => {
          alert('Age: ' + ageInput + ' // Gender: ' + genderInput);
          console.log('Age:' + ageInput);
          console.log('Gender:' + genderInput);
          //navigate('/')};
        }}
      >
        Weiter
      </Button>
    </BodyLayout>
  );
};

export default Result_2;
