import { Box, styled } from '@mui/material';

interface Props {
  children: React.ReactNode;
  my: string;
  mx: string;
}

export default function WithMargins({ children, my, mx }: Props) {
  const BoxWithMargins = styled(Box)`
    margin: ${my} ${mx};
    overflow-x: hidden;
    overflow-y: scroll;
    max-height: 75vh;
    text-align: left;
    padding-bottom: 100px;
  `;

  return <BoxWithMargins>{children}</BoxWithMargins>;
}
