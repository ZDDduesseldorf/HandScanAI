//external imports
import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useQuery } from '@apollo/client';

//internal imports
import { GET_SCAN_RESULT } from '@/services/queries';
import { GetScanResultData } from '@/services/graphqlTypes';
import { useAppStore } from '@/store/appStore';

//component imports
import WithMargins from '@/components/layout/WithMargins';
import Header from '@/components/custom/Header';
import NarrowFixedBottomRight from '@/components/buttons/NarrowFixedBottomRight';
import Centered from '@/components/layout/Centered';

/**
 * A page that is displayed during the calculation. As soon as the calculation
 * is complete, a button appears to navigate further.
 *
 * @returns Page that is displayed during the calculation
 */
export default function Processing() {
  /**
   * Method for changing the location
   * @see https://reactrouter.com/6.29.0/hooks/use-navigate
   */
  const navigate = useNavigate();

  /**
   * The scan entry stored in the React app store
   */
  const scanEntry = useAppStore((state) => state.scanEntry);

  /**
   * Gets the results of the scan from the backend and stores them in data.
   * loading is true while fetching the data.
   * error saves the error if one should occur
   */
  const { data, loading, error } = useQuery<GetScanResultData>(
    GET_SCAN_RESULT,
    {
      //get the data with the provided scan id
      variables: { id: scanEntry?.id },
      //do not execurte the query if there is no scan id
      skip: !scanEntry?.id,
    },
  );

  /**
   * Saves the scan result in the React app store
   */
  const { setScanResult } = useAppStore();

  /**
   * Saves the information of the nearest neighbours in the React
   * app store
   */
  const { setNearestNeighbours } = useAppStore();

  //update the data stored in the React app store if the data from the
  //backend changes (or if the setter functions change)
  useEffect(() => {
    //update classifier results
    if (data?.getScanResult.resultClassifier) {
      setScanResult(data.getScanResult.resultClassifier);
    }
    //update nearest neighbours
    if (data?.getScanResult.nearestNeighbourInfo) {
      setNearestNeighbours(data.getScanResult.nearestNeighbourInfo);
    }
  }, [data, setScanResult, setNearestNeighbours]);

  //if an error should occur, display the error
  //the application cannot proceed and the user should navigate back
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
        <NarrowFixedBottomRight onClick={() => void navigate('/result-1')}>
          Weiter
        </NarrowFixedBottomRight>
      )}
    </WithMargins>
  );
}
