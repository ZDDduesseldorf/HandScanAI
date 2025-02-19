import { Box, styled } from '@mui/material';

import Title from '@/components/headings/Title';

interface Props {
  title: string;
}

export default function Header({ title }: Props) {
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
}
