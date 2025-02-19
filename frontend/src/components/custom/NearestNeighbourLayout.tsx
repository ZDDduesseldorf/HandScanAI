import { Box, styled } from '@mui/material';

import { NearestNeighbour } from '@/services/graphqlTypes';

import Vertical from '../layout/Vertical';

interface Props {
  src: string | undefined;
  genderGuess: number;
  ageGuess: number;
  nearestNeighbours: NearestNeighbour[] | null;
}

export default function NearestNeighbourLayout({
  src,
  genderGuess,
  ageGuess,
  nearestNeighbours,
}: Props) {
  const HorizImageBox = styled(Box)`
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    margin: 3em 0;
    text-align: left;
  `;

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
      <img
        src="/ArrowRight.png"
        alt="Hand Scan AI Logo"
        style={{ objectFit: 'contain', alignSelf: 'center' }}
      />

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
            Hier war der <b>{neighbour.region}</b> sehr ähnlich zu deinem, daher
            hat HandScan mit Hilfe von diesem Bild dein Alter und Geschlecht
            bestimmt.
          </p>
        </Vertical>
      ))}
    </HorizImageBox>
  );
}
