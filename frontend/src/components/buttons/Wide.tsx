import { Button, styled } from '@mui/material';

interface Props {
  onClick: () => void;
  children: React.ReactNode;
}

export default function Wide({ onClick, children }: Props) {
  const Wide = styled(Button)`
    background-color: var(--primary);
    color: white;
    font-family: 'Delius Unicase', cursive;
    padding: 0.5em 1em;
    font-size: 1.5em;
    height: 2.5em;
    transition: background-color 0.3s;
    border-radius: 0;
    text-transform: none;
    &:hover {
      background-color: var(--primary-light);
    }
  `;

  return <Wide onClick={onClick}>{children}</Wide>;
}
