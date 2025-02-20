import { Typography, styled } from '@mui/material';

/**
 * Defines the typescript types of the parameters
 */
interface Props {
  children: React.ReactNode;
}

/**
 * Standardized component for a h2 heading with branded styling that is used
 * in combination with a primary heading/ title as subtitle.
 *
 * @param children Content of the heading
 * @returns Compontent with a h2 heading
 */
export default function Subtitle({ children }: Props) {
  /**
   * Styling for a mui <span> component that standardizes the primary
   * heading with the application's font, font size, font weight, color
   * and spacing.
   */
  const Subtitle = styled(Typography)`
    font-family: 'Inter', sans-serif;
    color: var(--primary);
    margin: 0 0 1.875rem;
    font-weight: 200;
    text-align: center;
    font-size: clamp(1rem, 2vw, 1.5rem);
  `;

  return <Subtitle variant="h2">{children}</Subtitle>;
}
