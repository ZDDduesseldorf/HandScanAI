import { Routes, Route, useLocation } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import Home from '@/pages/Home';
import PrivacyNotice from '@/pages/PrivacyNotice';
import ImageCapture from '@/pages/ImageCapture';
import ImagePostCapture from '@/pages/ImagePostCapture';
import Processing from '@/pages/Processing';
import SubmissionComplete from '@/pages/SubmissionComplete';
import Explanation from './pages/Explanation';
import Sandbox from '@/pages/Sandbox';
import BlackBox from '@/pages/BlackBox';
import Layout from './Layout';
import Result_1 from '@/pages/Result_1';
import Result_2 from '@/pages/Result_2';

import '@/assets/fonts.css';
import '@/App.css';

const App: React.FC = () => {
  const location = useLocation();

  const getPageVariants = (pathname: string) => {
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
              <Route path="/blackbox" element={<BlackBox />} />
              <Route path="/explanation" element={<Explanation />} />
              <Route path="/result-1" element={<Result_1 />} />
              <Route path="/result-2" element={<Result_2 />} />
              <Route
                path="/submission-complete"
                element={<SubmissionComplete />}
              />
            </Route>
            <Route path="/sandbox" element={<Sandbox />} />
          </Routes>
        </motion.div>
      </AnimatePresence>
    </div>
  );
};

export default App;
