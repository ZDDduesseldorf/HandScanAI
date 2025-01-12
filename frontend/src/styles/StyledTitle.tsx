import { styled } from '@mui/material';
import Typography from '@mui/material/Typography';

const StyledTitle = styled(Typography)`
  font-family: 'Delius Unicase', cursive;
  font-weight: 400;
  color: #1a3ab8;
  text-align: center;
  font-size: clamp(1.75rem, 4vw, 3.25rem);
  margin: 0;
`;

export default StyledTitle;
