import { Typography, Box, styled } from '@mui/material';

import Secondary from '../headings/Secondary';

interface Props {
  title?: string;
  text?: string;
  children?: React.ReactNode;
}

export default function WithText({ title, text, children }: Props) {
  const BgContainer = styled(Box)`
    background-color: var(--light-gray);
    border-radius: 1em;
    padding: 2em 3em;
    text-align: left;
  `;

  const BoxText = styled(Typography)`
    font-family: 'Inter', sans-serif;
    text-align: justify;
    font-weight: 200;
  `;

  return (
    <BgContainer>
      <Secondary>{title}</Secondary>
      <BoxText>{text}</BoxText>
      {children}
    </BgContainer>
  );
}
