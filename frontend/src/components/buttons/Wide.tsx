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
    padding: 20px 120px;
    font-size: clamp(0.875rem, 1.75vw, 1.25rem);
    width: clamp(10rem, 20vw, 18rem);
    height: 55px;
    transition: background-color 0.3s;
    text-transform: none;
    border-radius: 1rem;
    &:hover {
      background-color: var(--primary-light);
    }
  `;

  return <Wide onClick={onClick}>{children}</Wide>;
}
