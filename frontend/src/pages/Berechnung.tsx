import React from 'react';
// import { Typography, Container, Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import HorizStepper from '@/components/Stepper';

import './Berechnung.css';

const Berechnung: React.FC = () => {
  const navigate = useNavigate();

  return (
    <body>
      <style>
        @import
        url('https://fonts.googleapis.com/css2?family=Delius+Unicase:wght@400;700&display=swap');
      </style>

      <div className="top">
        <h2>Berechnung</h2>
        <img
          src="/HandLogo.png"
          alt="Logo von der Hand"
          //style={{ maxWidth: '30%', marginTop: '10px' }}
        />
      </div>

      <p>
        Ungefähr 90% der Menschen sind Rechtshänder, wobei die Handdominanz oft
        <br></br>
        in der frühen Kindheit festgelegt wird und teilweise genetisch<br></br>
        beeinflusst<br></br> ist.
      </p>

      <HorizStepper pageNumber={2}></HorizStepper>
    </body>
  );
};

export default Berechnung;
