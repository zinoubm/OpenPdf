import { Box } from '@mui/material';
import background from 'assets/images/auth/openpdf-background.svg';
import floating from 'assets/images/floating.png';
import './landingPage.css';

const LandingPageBackground = () => {
  return (
    <Box
      sx={{
        width: '100%',
        height: '110vh',
        position: 'absolute',
        overflow: 'hidden',
        zIndex: -1
      }}
    >
      <img
        src={background}
        className="hero-background"
        alt="openpdf-background"
        style={{ width: '150%', filter: 'blur(80px)', height: 'auto', position: 'absolute', top: '-28em', left: '6em', zIndex: 10 }}
      />
      <img
        className="hero-floating"
        src={floating}
        style={{ width: '45%', height: 'auto', position: 'relative', top: '10%', left: '52%', zIndex: 11 }}
        alt="floating"
      />
    </Box>
  );
};

export default LandingPageBackground;
