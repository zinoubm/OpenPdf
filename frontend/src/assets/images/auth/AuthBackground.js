import { Box } from '@mui/material';
import background from 'assets/images/auth/openpdf-background.svg';


const AuthBackground = () => {
  return (
    <Box sx={{ position: 'absolute', overflow: 'hidden', filter: 'blur(18px)', zIndex: -1, bottom: 0 }}>
      <div>
        <img src={background} alt="openpdf-background" style={{ width: '200%', height: 'auto', transform: 'translate(-200px, 60px)' }} />
      </div>
    </Box>
  );
};

export default AuthBackground;