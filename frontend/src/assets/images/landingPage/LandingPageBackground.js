import { Box } from '@mui/material';
import background from './heroBackground.png';

const LandingPageBackground = () => {
  return (
    <Box sx={{ position: 'absolute', overflow: 'hidden', zIndex: -1, bottom: 0 }}>
      <div>
        <img src={background} alt="openpdf-background" style={{ width: '150%', height: 'auto', transform: 'translate(-7em, 10em)' }} />
      </div>
    </Box>
  );
};

export default LandingPageBackground;
