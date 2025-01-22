import React, { useEffect } from 'react';
import { Typography, styled, Box } from '@mui/material';
import NavButton from '@/components/NavButton';
import { useQuery } from '@apollo/client';
import { HandScanResultQuery } from '@/services/queries';
import { HandData } from '@/services/graphqlTypes';
import { useDataContext } from '@/services/DataContext';

const CenteredInformationText = styled(Typography)`
  font-family: 'Delius Unicase', cursive;
  color: #1a3ab8;
  text-align: center;
  font-size: clamp(1rem, 2vw, 1.5rem);
  margin-bottom: 20px;
`;

const Processing: React.FC = () => {
  const { error, loading, data } = useQuery<{ getScanResult: HandData }>(
    HandScanResultQuery,
  );
  const { handData, setHandData } = useDataContext();

  useEffect(() => {
    if (data?.getScanResult) {
      setHandData(data.getScanResult);
    }
  }, [data, setHandData]);
  if (error) return <p>Error: {error.message}</p>;

  return (
    <Box>
      <CenteredInformationText>
        Ungefähr 90% der Menschen sind Rechtshänder,
        <br />
        wobei die Handdominanz oft in der frühen Kindheit <br />
        festgelegt wird und teilweise genetisch beeinflusst
        <br /> ist.
      </CenteredInformationText>
      <br></br>
      {/* {loading && <CircularProgress></CircularProgress>} */}
      {!loading && <NavButton RouteTo="/result-1">Weiter</NavButton>}
    </Box>
  );
};

export default Processing;
