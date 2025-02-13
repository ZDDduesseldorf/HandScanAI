import { styled } from '@mui/material/styles';
import Typography from '@mui/material/Typography';

export default function Subtitle(
    {children}:
    {children:string | React.ReactNode}
) {
    const Subtitle = styled(Typography)`
      font-family: 'Inter', sans-serif;
      color: var(--primary);
      margin: 0 0 1.875rem;
      font-weight: 200;
      text-align: center;
      font-size: 3em;
    `;
  
    return (
        <Subtitle variant="h2">{children}</Subtitle>
    );
  };