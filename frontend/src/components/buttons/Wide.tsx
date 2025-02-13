import { styled } from '@mui/material/styles';
import Button from '@mui/material/Button';

export default function Wide(
    {onClick,
        children
    }:
    {onClick:()=>void,
        children:string | React.ReactNode
    }
) {
    const Wide = styled(Button)`
        background-color: var(--primary);
        color: white;
        font-family: 'Delius Unicase', cursive;
        padding: 20px 120px;
        font-size: clamp(0.875rem, 1.75vw, 1.25rem);
        width: 360px;
        height: 55px;
        transition: background-color 0.3s;
        text-transform: none;

        &:hover {
            background-color: var(--primary-light);
        }
    `;
  
    return (
        <Wide onClick={onClick}>{children}</Wide>
    );
  };