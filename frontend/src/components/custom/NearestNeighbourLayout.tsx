import { Box, styled } from '@mui/material';

import { NearestNeighbour } from '@/services/graphqlTypes';

import Vertical from '../layout/Vertical';

/**
 * Defines the typescript types of the parameters
 */
interface Props {
  src: string | undefined;
  genderGuess: number;
  ageGuess: number;
  nearestNeighbours: NearestNeighbour[] | null;
}

/**
 * Displays the scan result with its nearest neighbours as images and
 * descriptive text on the explanation page.
 *
 * @param src Path to the captured image of the user
 * @param genderGuess The classified gender
 * @param ageGuess The classified age
 * @param nearestNeighbours List with the nearest neighbours
 * @returns Component to display the scan result with the nearest
 * neighbours
 */
export default function NearestNeighbourLayout({
  src,
  genderGuess,
  ageGuess,
  nearestNeighbours,
}: Props) {
  /**
   * Styling for a mui <div> component that provides a container for
   * the content. This component adds a flexbox to place images and
   * texts next to each other respectively.
   * Corresponding images and text are displayed one below the other
   * using a different component.
   */
  const HorizImageBox = styled(Box)`
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    margin: 3em 0;
    text-align: left;
  `;

  /**
   * Styling for a mui <div> component that contains the description of
   * of the user's captured image. The description is in the applications
   * primary color.
   */
  const HandText = styled(Box)`
    font-family: 'Delius Unicase', cursive;
    margin-top: 1.5rem;
    text-align: left;
    font-size: clamp(0.5rem, 2vw, 1rem);
    color: var(--primary);
  `;

  return (
    <HorizImageBox>
      <Vertical>
        <img
          src={src}
          alt="Captured"
          style={{ height: '200px', objectFit: 'contain' }}
        />
        <HandText>
          Dein Bild: <br></br> {genderGuess == 0 ? 'weiblich' : 'männlich'},{' '}
          {Math.round(ageGuess)}
        </HandText>
      </Vertical>
      <Vertical>
        <div style={{ height: '200px', flex: 'wrap', alignContent: 'center' }}>
          <img
            src="/ArrowRight.png"
            alt="Hand Scan AI Logo"
            style={{ objectFit: 'contain', alignSelf: 'center' }}
          />
        </div>
      </Vertical>
      {nearestNeighbours?.map((neighbour: NearestNeighbour, idx: number) => (
        <Vertical key={idx}>
          <img
            src={`http://localhost:8000/rest/image_nearest_neigbhours?image_id=${neighbour.id}`}
            style={{ height: '200px', objectFit: 'contain' }}
          />
          <HandText>
            {neighbour.gender == 0 ? 'weiblich' : 'männlich'}, {neighbour.age}
          </HandText>
          <p>
            Hier war {neighbour.region.toLowerCase() == 'hand' ? 'die' : 'der'}{' '}
            <b>{neighbour.region}</b> sehr ähnlich zu deinem, daher hat HandScan
            mit Hilfe von diesem Bild dein Alter und Geschlecht bestimmt.
          </p>
        </Vertical>
      ))}
    </HorizImageBox>
  );
}
