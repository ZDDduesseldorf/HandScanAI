import { Box, styled } from '@mui/material';

interface Props {
    children:React.ReactNode
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