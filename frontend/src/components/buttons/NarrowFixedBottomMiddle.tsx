import { Button, Box, styled } from '@mui/material';

interface Props {
  children: React.ReactNode;
  onClick: () => void;
}

export default function NarrowFixedBottomMiddle({ onClick, children }: Props) {
  const Container = styled(Box)`
    width: 100%;
    display: flex;
    justify-content: center;
  `;

  const NarrowFixedBottomMiddle = styled(Button)`
    background-color: var(--primary);
    border-radius: 0;
    color: white;
    font-family: 'Delius Unicase', cursive;
    position: fixed;
    bottom: 10vh;
    padding: 1em 1.5em;
    font-size: 1.5em;
    transition: background-color 0.3s;
    margin: auto;
    text-transform: none;
    font-size: 1.5em;
    height: 2.5em;
    &:hover {
      background-color: var(--primary-light);
    }
  `;

  return (
    <Container>
      <NarrowFixedBottomMiddle onClick={onClick}>
        {children}
      </NarrowFixedBottomMiddle>
    </Container>
  );
}
