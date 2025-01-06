import React, { ReactNode } from 'react';
import { Box, styled } from '@mui/material';
import StyledTitle from '@/styles/StyledTitle';

const HorizontalBar = styled(Box)`
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  max-width: 95%;
  margin: 1rem auto;
  padding: 0;
`;

const TitleBar: React.FC<{ children: ReactNode }> = ({ children }) => {
  return (
    <HorizontalBar>
      <StyledTitle variant="h1">{children}</StyledTitle>
      <img
        src="/HandLogo.png"
        alt="HandScan AI Logo"
        style={{ maxWidth: '12%', height: 'auto' }}
      />
    </HorizontalBar>
  );
};

export default TitleBar;
