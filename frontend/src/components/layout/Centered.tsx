import { styled } from '@mui/material/styles';
import Box from '@mui/material/Box';

interface Props {
  children:string | React.ReactNode
}

export default function Centered({children}:Props){
    const Centered = styled(Box)`
        display: flex;
        flex-direction: column;
        gap: 24px;
        width: 90%; /* Expands while keeping margins */
        max-width: 1000px; /* Prevents it from being too narrow */
        margin: 0 auto;
    `;
  
    return (
        <Centered>{children}</Centered>
    );
  };