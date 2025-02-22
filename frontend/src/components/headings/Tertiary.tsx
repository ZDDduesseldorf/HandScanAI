import { Typography, styled } from '@mui/material';

/**
 * Defines the typescript types of the parameters
 */
interface Props {
  children: React.ReactNode;
}

/**
 * Standardized component for a h3 (tertiary) heading with branded styling.
 *
 * @param children Content of the heading
 * @returns Compontent with a h3 heading
 */
export default function Tertiary({ children }: Props) {
  /**
   * Styling for a mui <span> component that standardizes the tertiary
   * heading with the application's font, font size and spacing.
   */
  const Tertiary = styled(Typography)`
    font-family: 'Delius Unicase', cursive;
    margin: 1em 0;
    text-align: left;
    font-size: clamp(1rem, 2vw, 1.5rem);
  `;

  return <Tertiary variant="h3">{children}</Tertiary>;
}
