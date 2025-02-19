import { Typography, styled } from '@mui/material';

interface Props {
  children: React.ReactNode;
}

export default function Tertiary({ children }: Props) {
  const Tertiary = styled(Typography)`
    font-family: 'Delius Unicase', cursive;
    margin: 1em 0;
    text-align: left;
    font-size: clamp(1rem, 2vw, 1.5rem);
  `;

  return <Tertiary variant="h3">{children}</Tertiary>;
}
