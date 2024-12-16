import React, { ReactNode } from 'react';
import { useNavigate } from 'react-router-dom';

import Button from '@mui/material/Button';
import styled from '@mui/material/styles/styled';

const CustomButton = styled(Button)({
  backgroundColor: '#0F3EB5',
  borderRadius: 0,
  variant: 'contained',
  color: 'white',
  disableElevation: true,
  fontFamily: 'Delius Unicase',
});

interface Props {
  children: ReactNode;
  RouteTo: string;
}

const NavButton: React.FC<Props> = ({ children, RouteTo }) => {
  const navigate = useNavigate();
  const handleClick = () => {
    navigate(RouteTo);
  };

  return (
    // JSX for your component goes here
    <CustomButton onClick={handleClick}>{children}</CustomButton>
  );
};

export default NavButton;
