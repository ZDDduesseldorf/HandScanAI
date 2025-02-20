import { Box, styled } from '@mui/material';

import Title from '@/components/headings/Title';

/**
 * Defines the typescript types of the parameters
 */
interface Props {
  title: string;
}

/**
 * Provides a branded header component for HandScan AI. A headline or
 * title is displayed in the header and the logo is added.
 *
 * @param title The title that is displayed in the header
 * @returns Component with the specified title and the HandScan AI logo
 */
export default function Header({ title }: Props) {
  /**
   * Styling for a mui <div> component that adds a container which
   * contains the headline and the logo.
   */
  const Container = styled(Box)`
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    margin: 1em auto;
    padding: 0;
    top: 0;
  `;

  return (
    <Container>
      <Title>{title}</Title>
      <img
        src="/HandLogo.png"
        alt="HandScan AI Logo"
        style={{ maxWidth: '12%', height: 'auto' }}
      />
    </Container>
  );
}
