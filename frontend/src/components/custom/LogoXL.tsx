import { styled } from '@mui/material';

interface Props {
  src: string;
  alt: string;
}

export default function Logo_XL({ src, alt }: Props) {
  const Logo = styled('img')`
    width: clamp(200px, 35%, 450px);
    margin-bottom: 1rem;
  `;

  return <Logo src={src} alt={alt} />;
}
