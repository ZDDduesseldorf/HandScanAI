import React from 'react';
import { Outlet, useLocation } from 'react-router-dom';
import { Box, styled } from '@mui/material';
import FooterStepper from '@/components/FooterStepper';
import TitleBar from '@/components/TitleBar';

const ScrollableBox = styled(Box)`
  margin: 20px 30px;
  overflow-y: auto;
  max-height: calc(100vh - 300px); /* Adjust based on your layout */
`;

const Layout: React.FC = () => {
  const location = useLocation();

  const stepMap: Record<string, number> = {
    '/privacy-notice': 0,
    '/image-capture': 1,
    '/processing': 2,
    '/result-1': 3,
    '/result-2': 3,
    '/blackbox': 3,
    '/submission-complete': 4,
  };

  const currentStep = stepMap[location.pathname] ?? -1; // Default to -1 if not found

  return (
    <Box>
      {/* Title Bar */}
      <TitleBar>HandScan AI</TitleBar>

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
