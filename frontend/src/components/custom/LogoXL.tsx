import { styled } from '@mui/material/styles';

interface Props {
    src:string,
    alt:string
}

export default function Logo_XL({src, alt}:Props){
    const Logo = styled('img')`
        width: 700px;
        margin-bottom: 1rem;
    `;
  
    return (
        <Logo src={src} alt={alt} />
    );
};