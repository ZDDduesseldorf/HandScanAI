import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from '@/pages/Home';
import About from '@/pages/About';
import Information from '@/pages/Information';
import '@/App.css';
import Berechnung from './pages/Berechnung';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="/information" element={<Information />} />
        <Route path="/berechnung" element={<Berechnung />} />
      </Routes>
    </Router>
  );
}

export default App;
