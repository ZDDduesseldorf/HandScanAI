import React from 'react';
import { Typography, TextField, MenuItem, Box, styled } from '@mui/material';
import { useNavigate } from 'react-router-dom';

import Header from '@/components/custom/Header';
import Secondary from '@/components/headings/Secondary';
import WithMargins from '@/components/layout/WithMargins';
import Justified from '@/components/text/Justified';
import NarrowBottomSticky from '@/components/buttons/NarrowBottomFixed';

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

const BoxText = styled(Typography)`
  font-family: 'Poppins', sans-serif;
  margin: 0 0 1 rem;
  text-align: justify;
  // font-size: clamp(1rem, 2vw, 1.5rem);
  font-size: 0.8rem;
`;

export default function Result_2(){
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

  const [ageInput, setAgeInput] = React.useState('');
  const [genderInput, setGenderInput] = React.useState('');

  return (
    <>
      <Header title="Ergebnis" />
      <WithMargins mx="2em" my="1.5em">
        <Secondary>KI kann Fehler machen</Secondary>
        <Justified>
          Auch wenn die KI leistungsstark ist, können Fehler auftreten. Überprüfe
          das Ergebnis, um sicherzugehen, dass es korrekt ist.
        </Justified>
        <BoxForm>
          <Secondary>Dein Alter</Secondary>
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
          <Secondary>Dein Geschlecht</Secondary>
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
        <NarrowBottomSticky onClick={() => {navigate('/submission-complete')}}>Weiter</NarrowBottomSticky>
      </WithMargins>
    </>
  );
};
