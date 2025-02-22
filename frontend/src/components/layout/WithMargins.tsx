import { Box, styled } from '@mui/material';

/**
 * Defines the typescript types of the parameters
 */
interface Props {
  children: React.ReactNode;
  my: string;
  mx: string;
}

/**
 * Container that accepts all types of React components as children. The
 * container has a definable margin. Overflowed content on the vertical
 * exis is kept and scrollable.
 *
 * @param children React components that are placed on the container
 * @param my Margin on the y-axis
 * @param mx Margin on the x-axis
 * @returns Component that adds a container with margins and keeps
 * overflowed content
 */
export default function WithMargins({ children, my, mx }: Props) {
  /**
   * Styling for the mui <div> element that add custom margin and keeps
   * overflowing content.
   */
  const BoxWithMargins = styled(Box)`
    margin: ${my} ${mx};
    overflow-x: hidden;
    overflow-y: scroll;
    max-height: 75vh;
    text-align: left;
    padding-bottom: 100px;
  `;

  return <BoxWithMargins>{children}</BoxWithMargins>;
}
