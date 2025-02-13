import { styled } from '@mui/material/styles';

export default function Logo_xl(
    {src, 
        alt}:
    {src:string,
        alt:string
    }
) {
    const Logo = styled('img')`
        width: 700px;
        margin-bottom: 1rem;
    `;
  
    return (
        <Logo src={src} alt={alt} />
    );
  };