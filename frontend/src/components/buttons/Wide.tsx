import { Button, styled } from '@mui/material';

interface Props {
  onClick: () => void;
  children: React.ReactNode;
  variant?: 'solid' | 'outlined';
}

export default function Wide({ onClick, children, variant = 'solid' }: Props) {
  const Wide = styled(Button)`
    background-color: var(--primary);
    color: white;
    font-family: 'Delius Unicase', cursive;
    padding: 0.5em 1em;
    font-size: 1.5em;
    height: 2.5em;
    transition: background-color 0.3s;
    border-radius: 0;
    text-transform: none;
    &:hover {
      background-color: var(--primary-light);
    }
  `;

  const WideOutlined = styled(Button)`
    border: 2px solid var(--primary);
    color: var(--primary);
    font-family: 'Delius Unicase', cursive;
    padding: 0.5em 1em;
    font-size: 1.5em;
    height: 2.5em;
    transition: background-color 0.3s;
    border-radius: 0;
    text-transform: none;
    background-color: transparent;
    &:hover {
      background-color: var(--primary-light);
    }
  `;

  return variant == 'outlined' ? (
    <WideOutlined onClick={onClick}>{children}</WideOutlined>
  ) : (
    <Wide onClick={onClick}>{children}</Wide>
  );
}
