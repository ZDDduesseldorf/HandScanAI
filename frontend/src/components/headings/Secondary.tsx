import { styled } from '@mui/material/styles';
import Typography from '@mui/material/Typography';

interface Props {
    children:string | React.ReactNode
}

export default function Secondary({children}:Props) {
    const Secondary = styled(Typography)`
      font-family: 'Delius Unicase', cursive;
      margin-bottom: 0.5rem;
      text-align: left;
      font-size: clamp(1.3rem, 2vw, 1.8rem);
    `;
  
    return (
        <Secondary variant="h2">{children}</Secondary>
    );
};