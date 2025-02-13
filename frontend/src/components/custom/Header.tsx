import { Box, styled } from '@mui/material';
import Title from '../headings/Title';

const HorizontalBar = styled(Box)`
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  max-width: 95%;
  margin: 1rem auto;
  padding: 0;
  top: 0;
`;
interface Props {
  title: string
}

export default function Header({title}:Props) {
  return (
    <HorizontalBar>
      <Title>{title}</Title>
      <img
        src="/HandLogo.png"
        alt="HandScan AI Logo"
        style={{ maxWidth: '12%', height: 'auto' }}
      />
    </HorizontalBar>
  );
};

