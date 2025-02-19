import React, { useState } from 'react';
import { TextField, MenuItem, Grid2 } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { useMutation } from '@apollo/client';

import { useAppStore } from '@/store/appStore';
import { UPDATE_SCAN_ENTRY } from '@/services/mutations';

import Header from '@/components/custom/Header';
import Secondary from '@/components/headings/Secondary';
import WithMargins from '@/components/layout/WithMargins';
import Justified from '@/components/text/Justified';
import NarrowFixedBottomRight from '@/components/buttons/NarrowFixedBottomRight';
import NarrowFixedBottomLeft from '@/components/buttons/NarrowFixedBottomLeft';
import WithText from '@/components/cards/WithText';

export default function Result_2() {
  const navigate = useNavigate();

  const genders = [
    {
      value: '0',
      label: 'weiblich',
    },
    {
      value: '1',
      label: 'männlich',
    },
  ];

  const [ageInput, setAgeInput] = useState('');
  const [genderInput, setGenderInput] = useState('');
  const scanId = useAppStore((state) => state.scanResult?.id);

  const [updateScanEntry] = useMutation(UPDATE_SCAN_ENTRY);
  
  const scanResult = useAppStore((state) => state.scanResult);
  
  if (!scanResult) {
    return (
      <p>Keine Daten vorhanden, Bitte gehen sie zur vorherigen Seite zurück</p>
    );
  }

  const handleSubmit = () => {
    updateScanEntry({
      variables: {
        id: scanId,
        input: {
          realAge: parseInt(ageInput, 10),
          realGender: parseInt(genderInput, 10),
          confirmed: true
        },
      },
    }).then(() => {
      navigate('/explanation')
    });
  };

  return (
    <WithMargins mx="2em" my="1.5em">
      <Header title="Ergebnis" />
      <Secondary>KI kann Fehler machen</Secondary>
      <Justified>
        Auch wenn die KI leistungsstark ist, können Fehler auftreten.
        Überprüfe das Ergebnis, um sicherzugehen, dass es korrekt ist.
      </Justified>
      <Grid2 container spacing={8}>
        <Grid2 size="grow">
          <WithText title="Dein Alter">
            <p>
              Wahrscheinlich bist du {Math.round(scanResult.classifiedAge)} Jahre alt. <br />
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
        <Grid2 size="grow">
          <WithText title="Dein Geschlecht">
            <p>
              Wahrscheinlich bist du {scanResult.classifiedGender == 0 ? "weiblich" : "männlich"}. <br />
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
      <NarrowFixedBottomLeft onClick={() => navigate(-1)}>
        Zurück
      </NarrowFixedBottomLeft>
      <NarrowFixedBottomRight onClick={handleSubmit}>
        Weiter
      </NarrowFixedBottomRight>
    </WithMargins>
  );
}
