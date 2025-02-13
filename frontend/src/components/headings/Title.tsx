import { styled } from '@mui/material/styles';
import Typography from '@mui/material/Typography';

export default function Title(
    {children}:
    {children:string | React.ReactNode}
) {
    const Title = styled(Typography)`
        font-family: 'Delius Unicase', cursive;
        font-weight: 400;
        color: var(--primary);
        margin: 0 0 0.625rem;
        text-align: center;
        font-size: 4em;
    `;
  
    return (
        <Title variant="h1">{children}</Title>
    );
  };