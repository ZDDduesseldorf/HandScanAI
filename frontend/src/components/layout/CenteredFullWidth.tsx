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
 * the y-axis. The child elements are stretched to the full width
 * of the container.
 *
 * @param children React components that are placed on the container
 * @param style Optional additional styles
 * @returns Component that adds a flex container that centers content
 */
export default function CenteredFullWidth({ children, style = '' }: Props) {
  /**
   * Styling for the mui <div> element that centers content on x- and
   * y-axis with a flex box while stretching the content and adds optional
   * custom styles.
   */
  const Centered = styled(Box)`
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100vh;
    width: 100vw;
    background-color: white;
    ${style}
  `;

  return <Centered>{children}</Centered>;
}
