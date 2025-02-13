import { styled } from '@mui/material/styles';
import Box from '@mui/material/Box';

interface Props {
    children:string | React.ReactNode
}

export default function CenteredFullWidth({children}: Props){
    const Centered = styled(Box)`
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 100vh;
        width: 100vw;
        background-color: white;
    `;
  
    return (
        <Centered>{children}</Centered>
    );
  };