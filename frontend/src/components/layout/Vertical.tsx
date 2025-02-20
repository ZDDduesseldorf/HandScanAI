import { Box, styled } from '@mui/material';

/**
 * Defines the typescript types of the parameters
 */
interface Props {
  children: React.ReactNode;
  style?: string;
}

/**
 * Container that arranges all elements passed to it vertically one
 * below the other.
 *
 * @param children React components that are placed on the container
 * @param style Optional additional styles
 * @returns Component that adds a flex container
 */
export default function Vertical({ children, style = '' }: Props) {
  /**
   * Styling for the mui <div> element that adds a flexbox with vertical
   * ordering and adds optional custom styles.
   */
  const Vertical = styled(Box)`
    display: flex;
    flex-direction: column;
    gap: 10px;
    align-content: flex-start;
    ${style}
  `;

  return <Vertical>{children}</Vertical>;
}
