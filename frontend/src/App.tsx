import {
  BrowserRouter as Router,
  Routes,
  Route,
  useLocation,
} from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import Home from '@/pages/Home';
import About from '@/pages/About';
import Information from '@/pages/Information';
import Berechnung from '@/pages/Berechnung';
import Bildaufnahme from '@/pages/Bildaufnahme';
import Sandbox from '@/pages/Sandbox';
import ErgebnisAge from '@/pages/ErgebnisAge';
import ErgebnisGender from './pages/ErgebnisGender';
import Danke from './pages/Danke';

import '@/assets/fonts.css';
import '@/App.css';

const App: React.FC = () => {
  const location = useLocation();

  // Define dynamic animation logic based on the current route
  const getPageVariants = (pathname: string) => {
    switch (pathname) {
      case '/':
        // Home: Opacity in, Move-left out
        return {
          initial: { opacity: 0 },
          animate: { opacity: 1, transition: { duration: 0.5 } },
          exit: { opacity: 0, x: '-100%', transition: { duration: 0.3 } },
        };
      case '/information':
        // Information: Move-left in, No animation out
        return {
          initial: { opacity: 0, x: '100%' },
          animate: { opacity: 1, x: 0, transition: { duration: 0.3 } },
          exit: {}, // No animation on exit
        };
      default:
        // All other pages: Instant transition (no animation)
        return {
          initial: {},
          animate: {},
          exit: {},
        };
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
            <Route path="/about" element={<About />} />
            <Route path="/information" element={<Information />} />
            <Route path="/berechnung" element={<Berechnung />} />
            <Route path="/bildaufnahme" element={<Bildaufnahme />} />
            <Route path="/sandbox" element={<Sandbox />} />
            <Route path="ergebnisage" element={<ErgebnisAge />} />
            <Route path="ergebnisgender" element={<ErgebnisGender />} />
            <Route path="danke" element={<Danke />} />
          </Routes>
        </motion.div>
      </AnimatePresence>
    </div>
  );
};

const AppWrapper: React.FC = () => (
  <Router>
    <App />
  </Router>
);

export default AppWrapper;
