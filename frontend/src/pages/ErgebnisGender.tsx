import React from 'react';
import { useNavigate } from 'react-router-dom';
import HorizStepper from '@/components/Stepper';
import TitleBar from '@/components/TitleBar';
import NavButton from '@/components/NavButton';

const ErgebnisGender: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div>
      <TitleBar>Ergebnis</TitleBar>
      <NavButton RouteTo="/Danke">Weiter</NavButton>
      <HorizStepper pageNumber={3}></HorizStepper>
    </div>
  );
};

export default ErgebnisGender;
