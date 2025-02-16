import { Typography, styled } from '@mui/material';

interface Props {
  children: React.ReactNode;
}

export default function Title({ children }: Props) {
  const Title = styled(Typography)`
    font-family: 'Delius Unicase', cursive;
    font-weight: 400;
    color: var(--primary);
    margin: 0 0 0.625rem;
    text-align: center;
    font-size: 4em;
  `;

  return <Title variant="h1">{children}</Title>;
}
