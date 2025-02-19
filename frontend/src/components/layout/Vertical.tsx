import { Box, styled } from '@mui/material';

interface Props {
  children: React.ReactNode;
  style?: string;
}

export default function Vertical({ children, style = '' }: Props) {
  const Vertical = styled(Box)`
    display: flex;
    flex-direction: column;
    gap: 10px;
    align-content: flex-start;
    ${style}
  `;

  return <Vertical>{children}</Vertical>;
}
