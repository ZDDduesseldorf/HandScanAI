import React from 'react';
import HorizStepper from '@/components/Stepper';
import TitleBar from '@/components/TitleBar';
import NavButton from '@/components/NavButton';
import { BodyLayout } from './Information';

const ErgebnisGender: React.FC = () => {
  return (
    <BodyLayout>
      <TitleBar>Ergebnis</TitleBar>
      <NavButton RouteTo="/Danke">Weiter</NavButton>
      <HorizStepper pageNumber={3}></HorizStepper>
    </BodyLayout>
  );
};

export default ErgebnisGender;
