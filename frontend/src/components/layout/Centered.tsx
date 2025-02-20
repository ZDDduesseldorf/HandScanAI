import { Box, styled } from '@mui/material';

/**
 * Defines the typescript types of the parameters
 */
interface Props {
  children: React.ReactNode;
  style?: string;
}

/**
 * Container that centers all elements passed to it in the middle
 * of the screen. The elements are centered on both the x-axis and
 * the y-axis.
 *
 * @param children React components that are placed on the container
 * @param style Optional additional styles
 * @returns Component that adds a flex container that centers content
 */
export default function Centered({ children, style = '' }: Props) {
  /**
   * Styling for the mui <div> element that centers content on x- and
   * y-axis with a flex box and adds optional custom styles.
   */
  const Centered = styled(Box)`
    display: flex;
    flex-direction: column;
    gap: 24px;
    width: 90%; /* Expands while keeping margins */
    max-width: 1000px; /* Prevents it from being too narrow */
    margin: 0 auto;
    ${style}
  `;

  return <Centered>{children}</Centered>;
}
