import { Button, styled } from '@mui/material';

/**
 * Defines the typescript types of the parameters
 */
interface Props {
  children: React.ReactNode;
  onClick: () => void;
}

/**
 * A narrow button that is fixed to the bottom left corner of the screen.
 *
 * @param onClick Action that is executed when the button is clicked
 * @param children Content of the button
 * @returns Button component that is fixed at the bottom left corner of the
 * screen
 */
export default function NarrowFixedBottomLeft({ onClick, children }: Props) {
  /**
   * Styling for a mui <button> component that adds a narrow (max-width 146px)
   * button that is fixed to the bottom left corner and adds a hover effect.
   */
  const NarrowFixedBottomLeft = styled(Button)`
    background-color: var(--primary);
    border-radius: 0;
    color: white;
    font-family: 'Delius Unicase', cursive;
    position: fixed;
    bottom: 10vh;
    left: 5vw;
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
    <NarrowFixedBottomLeft onClick={onClick}>{children}</NarrowFixedBottomLeft>
  );
}
