import {
  BrowserRouter as Router,
  Routes,
  Route,
  useLocation,
} from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import Home from '@/pages/Home';
import PrivacyNotice from '@/pages/PrivacyNotice';
import ImageCapture from '@/pages/ImageCapture';
import Processing from '@/pages/Processing';
import ResultsAge from '@/pages/ResultsAge';
import ResultsGender from '@/pages/ResultsGender';
import SubmissionComplete from '@/pages/SubmissionComplete';
import Sandbox from '@/pages/Sandbox';
import BlackBox from '@/pages/BlackBox';
import Layout from '@/components/Layout';

import '@/assets/fonts.css';
import '@/App.css';

import {
  ApolloClient,
  InMemoryCache,
  ApolloProvider,
  HttpLink,
  from,
} from '@apollo/client';
import { onError } from '@apollo/client/link/error';

const errorLink = onError(({ graphQLErrors, networkError }) => {
  if (graphQLErrors) {
    graphQLErrors.map(({ message, locations, path }) => {
      alert(`Graphql error ${message}`);
    });
  }
});

const link = from([
  errorLink,
  new HttpLink({ uri: 'http://localhost:6969/graphql' }), //ask salam for http address
]);

const client = new ApolloClient({
  cache: new InMemoryCache(),
  link: link, //according to documentation I could also put uri with graphql endpoint here
});

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
              <Route path="/processing" element={<Processing />} />
              <Route path="/results-age" element={<ResultsAge />} />
              <Route path="/results-gender" element={<ResultsGender />} />
              <Route path="/blackbox" element={<BlackBox />} />
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

// added Apollo Wrapper below
const AppWrapper: React.FC = () => (
  <ApolloProvider client={client}>
    <Router>
      <App />
    </Router>
  </ApolloProvider>
);

export default AppWrapper;
