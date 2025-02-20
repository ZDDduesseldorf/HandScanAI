//external imports
import React from 'react';
import { Outlet, useLocation } from 'react-router-dom';
import { Box, styled } from '@mui/material';

//component imports
import FooterStepper from '@/components/navigation/Stepper';

// Scrollable box to contain the page content
const ScrollableBox = styled(Box)`
  margin: 20px 30px;
  overflow-y: auto;
`;

/**
 * Layout component that wraps page content with a common structure.
 *
 * It renders a scrollable content area for nested routes using React Router's <Outlet />
 * and conditionally displays a FooterStepper based on the current route.
 *
 * The stepMap object defines which step to show in the FooterStepper for specific routes.
 *
 */
const Layout: React.FC = () => {
  /**
   * Retrieves the current location from React Router
   * @see https://reactrouter.com/v6/hooks/use-location
   */
  const location = useLocation();

  /**
   * A mapping of route paths to their corresponding step numbers for the FooterStepper.
   *
   * Each key represents a route, and the value indicates the step number to be displayed.
   * If the current route does not exist in this map, a default of -1 is used, indicating
   * that the FooterStepper should not be shown.
   */
  const stepMap: Record<string, number> = {
    '/privacy-notice': 0,
    '/image-capture': 1,
    '/image-post-capture': 1,
    '/processing': 2,
    '/result-1': 3,
    '/result-2': 3,
    '/explanation': 4,
  };

  /**
   * Determines the current step number based on the current route.
   * Defaults to -1 if the pathname is not found, indicating that the FooterStepper should not be shown.
   */
  const currentStep = stepMap[location.pathname] ?? -1;

  return (
    <Box>
      {/* Page Content */}
      <ScrollableBox>
        <Outlet />
      </ScrollableBox>

      {/* Stepper - Only show if step is valid */}
      {currentStep !== -1 && <FooterStepper pageNumber={currentStep} />}
    </Box>
  );
};

export default Layout;
