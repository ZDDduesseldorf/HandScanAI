import { Box, styled } from '@mui/material';

interface Props {
  children:React.ReactNode,
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