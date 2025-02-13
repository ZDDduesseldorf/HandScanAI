import { useNavigate } from 'react-router-dom';

import Centered from '@/components/layout/Centered';
import Logo_xl from '@/components/custom/Logo_xl';
import Title from '@/components/headings/Title';
import Subtitle from '@/components/headings/Subtitle';
import WideButton from '@/components/buttons/Wide';

export default function Home () {
  const navigate = useNavigate();

  return (
    <Centered>
      <Logo_xl src="/logo.png" alt="Hand Scan AI Logo"/>
      <Title>Hand Scan AI</Title>
      <Subtitle>Scan it. Know it.</Subtitle>
      <WideButton onClick={() => navigate('/privacy-notice')}>Start</WideButton>
      <WideButton onClick={() => navigate("/explanation")}>Debug Explanation</WideButton>
    </Centered>
  );
};
