import { Box, styled } from '@mui/material';

import { NearestNeighbour } from '@/services/graphqlTypes';

interface Props {
  src:string | undefined;
  nearestNeighbours:NearestNeighbour[] | null;
}

export default function NearestNeighbourLayout({ src, nearestNeighbours }: Props) {
    const HorizImageBox = styled(Box)`
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    margin-top: 20px;
    // objectFit: contain;
  }
  `;
  const HandText = styled(Box)`
  font-family: 'Delius Unicase', cursive;
  margin-top: 1.5rem;
  text-align: left;
  font-size: clamp(0.5rem, 2vw, 1rem);
  color: #0F3EB5;
  }
  `;
  const VerticalElements = styled(Box)`
  display: flex;
  flex-direction: column;
  justify-content: center;
}
`;

  return (
    <HorizImageBox>
        <VerticalElements>
          <img
            src={src}
            alt="Captured"
            style={{ maxWidth: '400px', borderRadius: '8px' }}
          />
          <HandText>
            Dein Bild: <br></br> Weiblich, 28
          </HandText>
        </VerticalElements>
        <img src="/ArrowRight.png" alt="Hand Scan AI Logo" />
        {
            nearestNeighbours?.map((neighbour:NearestNeighbour) => 
            <VerticalElements>
                <img 
                    src={`http://localhost:8000/rest/image_nearest_neigbhours?image_id=${neighbour.id}`}
                    style={{ maxWidth: '200px'}}/>
                <HandText>{neighbour.gender}, {neighbour.age}</HandText>
            </VerticalElements>)
        }
      </HorizImageBox>
  );
}
