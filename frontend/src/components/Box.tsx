import * as React from 'react';
import { ReactNode } from 'react';
import Box from '@mui/material/Box';

interface Props {
  children: ReactNode;
}

const BoxSx: React.FC<Props> = ({ children }) => {
  return (
    <Box
      sx={{
        // width: 400,
        // height: 400,
        borderRadius: 5, // rounded corner
        bgcolor: '#d9d9d9',
        display: 'flex', // Center the text both vertically and horizontally
        flexDirection: 'column', // Stacks header and paragraph vertically
        alignItems: 'left',
        justifyContent: 'space-between',
        padding: 2,
        overflow: 'auto', // Adds scroll if content overflows
        '&:hover': {
          bgcolor: '#d9d9d9', // keeping color when hovering the same
        },
      }}
    >
      {children}
    </Box>
  );
};

export default BoxSx;
