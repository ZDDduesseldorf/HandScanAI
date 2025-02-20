import { styled } from '@mui/material';

/**
 * Defines the typescript types of the parameters
 */
interface Props {
  src: string;
  alt: string;
}

/**
 * The HandScanAI logo in large size.
 *
 * @param src Path to the logo
 * @param alt Alternative image text
 * @returns Image component containing the HandScanAI logo
 */
export default function Logo_XL({ src, alt }: Props) {
  /**
   * Styling for a mui <img> component that sizes the logo
   * and adds some margin.
   */
  const Logo = styled('img')`
    width: clamp(200px, 35%, 450px);
    margin-bottom: 1rem;
  `;

  return <Logo src={src} alt={alt} />;
}
