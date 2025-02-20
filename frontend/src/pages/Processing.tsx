import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useQuery } from '@apollo/client';

import { GET_SCAN_RESULT } from '@/services/queries';
import { GetScanResultData } from '@/services/graphqlTypes';
import { useAppStore } from '@/store/appStore';

import WithMargins from '@/components/layout/WithMargins';
import Header from '@/components/custom/Header';
import NarrowFixedBottomRight from '@/components/buttons/NarrowFixedBottomRight';
import Centered from '@/components/layout/Centered';

export default function Processing() {
  const navigate = useNavigate();
  const scanEntry = useAppStore((state) => state.scanEntry);

  const { data, loading, error } = useQuery<GetScanResultData>(
    GET_SCAN_RESULT,
    {
      variables: { id: scanEntry?.id },
      skip: !scanEntry?.id,
    },
  );
  const { setScanResult } = useAppStore();
  const { setNearestNeighbours } = useAppStore();

  useEffect(() => {
    if (data?.getScanResult.resultClassifier) {
      setScanResult(data.getScanResult.resultClassifier);
    }
    if (data?.getScanResult.nearestNeighbourInfo) {
      setNearestNeighbours(data.getScanResult.nearestNeighbourInfo);
    }
  }, [data, setScanResult, setNearestNeighbours]);

  if (error) return <p>Error: {error.message}</p>;

  return (
    <WithMargins mx="2em" my="1.5em">
      <Header title="Berechnung" />
      <Centered
        style="
          color: var(--primary);
          font-family: 'Delius Unicase', cursive;
          text-align: center;
          font-size: 1.5em;
          padding-top: 5em;
        "
      >
        Das k-Nearest Neighbors (k-NN) Modell hinter HandScan AI analysiert die
        Merkmale eines Bildes und vergleicht sie mit denen der nächsten k
        Nachbarn, also Bildern, in seiner Datenbank, um die Vorhersage zu
        treffen.
      </Centered>
      <br></br>
      {!loading && (
        <NarrowFixedBottomRight onClick={() => navigate('/result-1')}>
          Weiter
        </NarrowFixedBottomRight>
      )}
    </WithMargins>
  );
}
