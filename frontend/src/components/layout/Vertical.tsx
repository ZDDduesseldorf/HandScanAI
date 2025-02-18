import { Box, styled } from '@mui/material';

interface Props {
  children: React.ReactNode;
}

export default function Vertical({ children }: Props) {
  const Vertical = styled(Box)`
    display: flex;
    flex-direction: column;
    gap: 10px;
    align-content: flex-start;
  `;

  return <Vertical>{children}</Vertical>;
}
