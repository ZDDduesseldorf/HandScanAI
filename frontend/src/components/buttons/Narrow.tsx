import { styled } from '@mui/material/styles';
import Button from '@mui/material/Button';

export default function Narrow(
  {onClick,
      children
  }:
  {onClick:()=>void,
      children:string | React.ReactNode
  }
) {
    const Narrow = styled(Button)`
        background-color: var(--primary);
        color: white;
        font-family: 'Delius Unicase', cursive;
        padding: 16px 24px;
        font-size: 1.5em;
        width: 146px;
        height: 62px;
        transition: background-color 0.3s;
        text-transform: none;

        &:hover {
            background-color: var(--primary-light);
        }
    `;
  
    return (
        <Narrow onClick={onClick}>{children}</Narrow>
    );
  };