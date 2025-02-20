import { Typography, Box, styled } from '@mui/material';

import Secondary from '../headings/Secondary';

/**
 * Defines the typescript types of the parameters
 */
interface Props {
  title?: string;
  text?: string;
  children?: React.ReactNode;
}

/**
 * A card that displays some text. The card has a title and a text below
 * the title. Optional additional content can be inserted.
 *
 * @param title Optional Title of the card
 * @param text Optional text content of the card
 * @param children Optional additional content of the card
 * @returns Card component which displays given content in a visual box
 */
export default function WithText({ title, text, children }: Props) {
  /**
   * Styling for a mui <div> component that adds a container with a
   * background color to make the card visible.
   */
  const Container = styled(Box)`
    background-color: var(--light-gray);
    border-radius: 1em;
    padding: 2em 3em;
    text-align: left;
  `;

  /**
   * Styling for a mui <p> component that justifies the text inside the
   * card.
   */
  const BoxText = styled(Typography)`
    font-family: 'Inter', sans-serif;
    text-align: justify;
    font-weight: 200;
  `;

  return (
    <Container>
      <Secondary>{title}</Secondary>
      <BoxText>{text}</BoxText>
      {children}
    </Container>
  );
}
