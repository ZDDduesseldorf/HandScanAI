import { Box, styled } from '@mui/material';

interface Props {
  children: React.ReactNode;
}

export default function Horizontal({ children }: Props) {
  const Horizontal = styled(Box)`
    display: flex;
    flex-direction: row;
    gap: 10px;
  `;

  return <Horizontal>{children}</Horizontal>;
}
