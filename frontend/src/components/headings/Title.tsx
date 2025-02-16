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
    font-size: clamp(1.75rem, 4vw, 3.25rem);
  `;

  return <Title variant="h1">{children}</Title>;
}
