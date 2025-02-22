import { styled } from '@mui/material/styles';
import Typography from '@mui/material/Typography';

/**
 * Defines the typescript types of the parameters
 */
interface Props {
  children: React.ReactNode;
}

/**
 * Centers text and components that can be placed within a <p> element
 *
 * @param children Text or React components that can be placed within a <p>
 *  element that is to be centered
 * @returns Component that displays centered text
 */
export default function Centered({ children }: Props) {
  /**
   * Styling for a mui <p> component that centers text
   */
  const Text = styled(Typography)`
    margin: 1em 0;
    font-family: 'Poppins', sans-serif;
    text-align: centered;
  `;

  return <Text>{children}</Text>;
}
