import { Typography, styled } from '@mui/material';

interface Props {
  children: React.ReactNode;
  centered?: boolean;
  style?: string;
}

export default function Secondary({
  children,
  centered = false,
  style = '',
}: Props) {
  const Secondary = styled(Typography)`
    font-family: 'Delius Unicase', cursive;
    font-size: clamp(1.3rem, 2vw, 1.8rem);
    margin-bottom: 1em;
    ${centered ? 'text-align: center;' : 'text-align: left;'}
    ${style}
  `;

  return <Secondary variant="h2">{children}</Secondary>;
}
