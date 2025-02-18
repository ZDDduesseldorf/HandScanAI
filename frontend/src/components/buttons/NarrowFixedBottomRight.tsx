import { Button, styled } from '@mui/material';

interface Props {
  children: React.ReactNode;
  onClick: () => void;
}

export default function NarrowFixedBottomRight({ onClick, children }: Props) {
  const NarrowFixedBottomRight = styled(Button)`
    background-color: var(--primary);
    border-radius: 0;
    color: white;
    font-family: 'Delius Unicase', cursive;
    position: fixed;
    bottom: 10vh;
    right: 5vw;
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

  return <NarrowFixedBottomRight onClick={onClick}>{children}</NarrowFixedBottomRight>;
}
