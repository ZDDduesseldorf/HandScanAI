import { Box, styled } from '@mui/material';

interface Props {
  children: React.ReactNode;
  style?: string;
}

export default function CenteredFullWidth({ children, style = '' }: Props) {
  const Centered = styled(Box)`
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100vh;
    width: 100vw;
    background-color: white;
    ${style}
  `;

  return <Centered>{children}</Centered>;
}
