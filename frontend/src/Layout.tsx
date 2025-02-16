import React from 'react';
import { Outlet, useLocation } from 'react-router-dom';
import { Box, styled } from '@mui/material';
import FooterStepper from '@/components/navigation/Stepper';

const ScrollableBox = styled(Box)`
  margin: 20px 30px;
  overflow-y: auto;
`;

const Layout: React.FC = () => {
  const location = useLocation();

  const stepMap: Record<string, number> = {
    '/privacy-notice': 0,
    '/image-capture': 1,
    '/image-post-capture': 1,
    '/processing': 2,
    '/result-1': 3,
    '/result-2': 3,
    '/blackbox': 3,
    '/submission-complete': 4,
  };

  const currentStep = stepMap[location.pathname] ?? -1; // Default to -1 if not found

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
