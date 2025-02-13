import { styled } from '@mui/material/styles';
import Box from '@mui/material/Box';

export default function Centered(
    {children}:
    {children:string | React.ReactNode}
) {
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