import { Button, styled } from '@mui/material';

interface Props {
  children: React.ReactNode;
  onClick: ()=>void;
}

export default function NarrowBottomFixed ({ onClick, children }:Props){
  const NarrowBottomFixed = styled(Button)`
    background-color: var(--primary);
    border-radius: 0;
    color: white;
    font-family: 'Delius Unicase', cursive;
    position: fixed;
    bottom: 120px;
    right: 80px;
    padding: 16px 24px;
    font-size: 1.5em;
    width: 146px;
    height: 62px;
    transition: background-color 0.3s;
    text-transform: none;

    &:hover {
        background-color: var(--primary-light);
    }
  `;

  return (
    <NarrowBottomFixed onClick={onClick}>{children}</NarrowBottomFixed>
  );
};
