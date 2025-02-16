import { Typography, styled } from '@mui/material';

interface Props {
  children: string | React.ReactNode;
}

export default function Subtitle({ children }: Props) {
  const Subtitle = styled(Typography)`
    font-family: 'Inter', sans-serif;
    color: var(--primary);
    margin: 0 0 1.875rem;
    font-weight: 200;
    text-align: center;
    font-size: clamp(1rem, 2vw, 1.5rem);
  `;

  return <Subtitle variant="h2">{children}</Subtitle>;
}
