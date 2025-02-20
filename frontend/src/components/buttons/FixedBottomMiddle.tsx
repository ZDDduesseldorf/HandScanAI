import { Button, Box, styled } from '@mui/material';

/**
 * Defines the typescript types of the parameters
 */
interface Props {
  children: React.ReactNode;
  onClick: () => void;
}

/**
 * A narrow button that is fixed at the bottom center of the screen.
 *
 * @param onClick Action that is executed when the button is clicked
 * @param children Content of the button
 * @returns Button component that is fixed at the bottom center of the
 * screen
 */
export default function FixedBottomMiddle({ onClick, children }: Props) {
  /**
   * Styling for a mui <div> component that adds a container around the button
   * to center it.
   */
  const Container = styled(Box)`
    width: 100%;
    display: flex;
    justify-content: center;
  `;

  /**
   * Styling for a mui <button> component that adds a button that is fixed to
   * the bottom and adds a hover effect.
   */
  const FixedBottomMiddle = styled(Button)`
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
      <FixedBottomMiddle onClick={onClick}>{children}</FixedBottomMiddle>
    </Container>
  );
}
