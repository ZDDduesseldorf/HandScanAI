import { Box, styled } from '@mui/material';
import * as React from 'react';
import { ReactNode } from 'react';
import { Title } from '@/pages/Home';

interface Props {
  children: ReactNode;
}

const HorizontalBar = styled(Box)`
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  margin: 0 auto;
`;

const TitleBar: React.FC<Props> = ({ children }) => {
  return (
    <HorizontalBar>
      <Title variant="h1">{children}</Title>
      <img
        src="/HandLogo.png"
        alt="Logo von der Hand"
        style={{ maxWidth: '12%' }}
      />
    </HorizontalBar>
  );
};

export default TitleBar;
