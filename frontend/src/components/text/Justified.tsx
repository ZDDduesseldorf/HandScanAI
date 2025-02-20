import { styled } from '@mui/material/styles';
import Typography from '@mui/material/Typography';

/**
 * Defines the typescript types of the parameters
 */
interface Props {
  children: React.ReactNode;
}

/**
 * Justfies text and components that can be placed within a <p> element
 *
 * @param children Text or React components that can be placed within a <p>
 *  element that is to be justified
 * @returns Component that displays justified text
 */
export default function Justified({ children }: Props) {
  /**
   * Styling for a mui <p> component that justifies text
   */
  const Text = styled(Typography)`
    margin: 1em 0;
    text-align: justify;
  `;

  return <Text>{children}</Text>;
}
