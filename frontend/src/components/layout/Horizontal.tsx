import { Box, styled } from '@mui/material';

interface Props {
  children: React.ReactNode;
  margin?: string;
}

export default function Horizontal({ children, margin }: Props) {
  const Horizontal = styled(Box)`
    display: flex;
    flex-direction: row;
    gap: 10px;
    margin: ${margin ? margin : 'auto'};
  `;

  return <Horizontal>{children}</Horizontal>;
}
