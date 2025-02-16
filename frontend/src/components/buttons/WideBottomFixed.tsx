import { Button, styled } from '@mui/material';

interface Props {
  onClick: () => void;
  children: React.ReactNode;
}

export default function WideBottomFixed({ onClick, children }: Props) {
  const WideBottomFixed = styled(Button)`
    background-color: var(--primary);
    color: white;
    font-family: 'Delius Unicase', cursive;
    padding: 20px 120px;
    font-size: clamp(0.875rem, 1.75vw, 1.25rem);
    width: 360px;
    height: 55px;
    transition: background-color 0.3s;
    position: fixed;
    bottom: 120px;
    margin: auto;
    text-transform: none;
    border-radius: 0;
    &:hover {
      background-color: var(--primary-light);
    }
  `;

  return <WideBottomFixed onClick={onClick}>{children}</WideBottomFixed>;
}
