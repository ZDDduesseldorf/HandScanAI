import React, { useEffect } from 'react';
import { Typography, styled, Box } from '@mui/material';
import NavButton from '@/components/buttons/Navigation';
import { useQuery } from '@apollo/client';
import { GET_SCAN_RESULT } from '@/services/queries';
import { GetScanResultData } from '@/services/graphqlTypes';
import { useAppStore } from '@/store/appStore';

const CenteredInformationText = styled(Typography)`
  font-family: 'Delius Unicase', cursive;
  color: #1a3ab8;
  text-align: center;
  font-size: clamp(1rem, 2vw, 1.5rem);
  margin-bottom: 20px;
`;

const Processing: React.FC = () => {
  const scanEntry = useAppStore((state) => state.scanEntry);

  const { data, loading, error } = useQuery<GetScanResultData>(
    GET_SCAN_RESULT,
    {
      variables: { id: scanEntry?.id },
      skip: !scanEntry?.id,
    },
  );
  const { setScanResult } = useAppStore();

  useEffect(() => {
    if (data?.getScanResult) {
      setScanResult(data.getScanResult);
    }
  }, [data, setScanResult]);
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
