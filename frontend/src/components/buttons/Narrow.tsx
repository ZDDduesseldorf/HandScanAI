import { Button, styled } from '@mui/material';

interface Props {
    onClick: () => void,
    children: React.ReactNode
}

export default function Narrow({onClick, children}:Props){
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