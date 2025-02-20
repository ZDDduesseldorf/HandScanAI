import { Typography, styled } from '@mui/material';

/**
 * Defines the typescript types of the parameters
 */
interface Props {
  children: React.ReactNode;
  centered?: boolean;
  style?: string;
}

/**
 * Standardized component for a h2 (secondary) heading with branded styling.
 *
 * @param children Content of the heading
 * @param centered True, if the heading should be centered, default: false
 * @param style Optional additional styles
 * @returns Compontent with a h2 heading
 */
export default function Secondary({
  children,
  centered = false,
  style = '',
}: Props) {
  /**
   * Styling for a mui <span> component that standardizes the secondary
   * heading with the application's font, font size and spacing.
   */
  const Secondary = styled(Typography)`
    font-family: 'Delius Unicase', cursive;
    font-size: clamp(1.3rem, 2vw, 1.8rem);
    margin-bottom: 1em;
    ${centered ? 'text-align: center;' : 'text-align: left;'}
    ${style}
  `;

  return <Secondary variant="h2">{children}</Secondary>;
}
