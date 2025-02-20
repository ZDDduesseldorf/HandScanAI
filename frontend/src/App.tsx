//external imports
import { Routes, Route, useLocation } from 'react-router-dom';
import { motion, AnimatePresence, Variants } from 'framer-motion';

//internal imports
import '@/assets/fonts.css';
import '@/App.css';

//page imports
import Home from '@/pages/Home';
import PrivacyNotice from '@/pages/PrivacyNotice';
import ImageCapture from '@/pages/ImageCapture';
import ImagePostCapture from '@/pages/ImagePostCapture';
import Processing from '@/pages/Processing';
import SubmissionComplete from '@/pages/SubmissionComplete';
import Explanation from '@/pages/Explanation';
import Result_1 from '@/pages/Result_1';
import Result_2 from '@/pages/Result_2';
import Layout from '@/Layout';

/**
 * The App component sets up the routing structure and page transition animations for HandScanAI.
 *
 * It leverages React Router to define application routes and Framer Motion's AnimatePresence and motion components
 * to animate the entry and exit transitions between pages.
 *
 */
const App: React.FC = () => {
  /**
   * Retrieves the current location object from React Router
   * @see https://reactrouter.com/v6/hooks/use-location
   */
  const location = useLocation();

  /**
   * Returns animation variants based on the current pathname.
   *
   * This function provides specific animation configurations for defined routes:
   * - For the home route ('/'): fades in the page and slides it out to the left on exit.
   * - For the privacy notice route ('/privacy-notice'): slides the page in from the right.
   * - For all other routes: no specific animation variants are applied.
   *
   * @param {string} pathname - The current path from the location object.
   * @returns A Variants object containing `initial`, `animate`, and `exit` properties for motion animations.
   */
  const getPageVariants = (pathname: string): Variants => {
    switch (pathname) {
      case '/':
        return {
          initial: { opacity: 0 },
          animate: { opacity: 1 },
          exit: { opacity: 0, x: '-100%' },
        };
      case '/privacy-notice':
        return {
          initial: { opacity: 0, x: '100%' },
          animate: { opacity: 1, x: 0 },
          exit: {},
        };
      default:
        return { initial: {}, animate: {}, exit: {} };
    }
  };

  return (
    <div className="page-wrapper">
      <AnimatePresence mode="wait">
        <motion.div
          key={location.pathname}
          variants={getPageVariants(location.pathname)}
          initial="initial"
          animate="animate"
          exit="exit"
          className="page"
        >
          <Routes location={location}>
            <Route path="/" element={<Home />} />
            <Route element={<Layout />}>
              <Route path="/privacy-notice" element={<PrivacyNotice />} />
              <Route path="/image-capture" element={<ImageCapture />} />
              <Route
                path="/image-post-capture"
                element={<ImagePostCapture />}
              />
              <Route path="/processing" element={<Processing />} />
              <Route path="/explanation" element={<Explanation />} />
              <Route path="/result-1" element={<Result_1 />} />
              <Route path="/result-2" element={<Result_2 />} />
              <Route
                path="/submission-complete"
                element={<SubmissionComplete />}
              />
            </Route>
          </Routes>
        </motion.div>
      </AnimatePresence>
    </div>
  );
};

export default App;
