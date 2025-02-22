import { Typography, styled } from '@mui/material';

/**
 * Defines the typescript types of the parameters
 */
interface Props {
  children: React.ReactNode;
}

/**
 * Standardized component for a h1 (primary) heading (aka title) with
 * branded styling.
 *
 * @param children Content of the heading
 * @returns Compontent with a h1 heading
 */
export default function Title({ children }: Props) {
  /**
   * Styling for a mui <span> component that standardizes the primary
   * heading with the application's font, font size, font weight, color
   * and spacing.
   */
  const Title = styled(Typography)`
    font-family: 'Delius Unicase', cursive;
    font-weight: 400;
    color: var(--primary);
    margin: 0 0 0.625rem;
    text-align: center;
    font-size: clamp(1.75rem, 4vw, 3.25rem);
  `;

  return <Title variant="h1">{children}</Title>;
}
