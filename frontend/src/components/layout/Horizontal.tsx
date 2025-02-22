import { Box, styled } from '@mui/material';

/**
 * Defines the typescript types of the parameters
 */
interface Props {
  children: React.ReactNode;
  margin?: string;
  style?: string;
}

/**
 * Container that arranges all elements passed to it horizontally
 * next to the other.
 *
 * @param children React components that are placed on the container
 * @param margin Optional margin of the container
 * @param style Optional additional styles
 * @returns Component that adds a flex container
 */
export default function Horizontal({ children, margin, style = '' }: Props) {
  /**
   * Styling for the mui <div> element that adds a flexbox with horizontal
   * ordering and adds optional custom styles.
   */
  const Horizontal = styled(Box)`
    display: flex;
    flex-direction: row;
    gap: 10px;
    margin: ${margin ?? '0'};
    ${style};
  `;

  return <Horizontal>{children}</Horizontal>;
}
