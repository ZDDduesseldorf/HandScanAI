import Button from '@mui/material/Button';
import { styled } from '@mui/material/styles';

interface Props {
  children: React.ReactNode;
  onClick: ()=>void;
}

export default function NarrowBottomSticky ({ onClick, children }:Props){
  const NarrowBottomSticky = styled(Button)`
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
    <NarrowBottomSticky onClick={onClick}>{children}</NarrowBottomSticky>
  );
};
