import { Box, styled } from '@mui/material';

interface Props {
  children: React.ReactNode;
  margin?: string;
  style?: string;
}

export default function Horizontal({ children, margin, style = '' }: Props) {
  const Horizontal = styled(Box)`
    display: flex;
    flex-direction: row;
    gap: 10px;
    margin: ${margin ?? '0'};
    ${style};
  `;

  return <Horizontal>{children}</Horizontal>;
}
