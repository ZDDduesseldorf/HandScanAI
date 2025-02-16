import { styled } from '@mui/material/styles';
import Typography from '@mui/material/Typography';

interface Props {
  children: string | React.ReactNode;
}

export default function Justified({ children }: Props) {
  const Text = styled(Typography)`
    margin: 1em 0;
    font-family: 'Poppins', sans-serif;
    text-align: justify;
  `;

  return <Text>{children}</Text>;
}
