import { styled } from '@mui/material/styles';
import Box from '@mui/material/Box';

interface Props {
  children:string | React.ReactNode,
  my:string,
  mx:string
}

export default function WithMargins({children, my, mx}:Props){
  const BoxWithMargins = styled(Box)`
    margin: ${my} ${mx};
  `;
  
    return (
        <BoxWithMargins>{children}</BoxWithMargins>
    );
  };