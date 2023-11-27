import { Box, useMediaQuery } from '@mui/material';
import Logo from 'components/Logo';
import Profile from './Profile';
import FileUploader from './FileUploader/index';
import Upgrade from './Upgrade/index';
import MobileSection from './MobileSection';

const HeaderContent = () => {
  const matchesXs = useMediaQuery((theme) => theme.breakpoints.down('md'));

  return (
    <>
      <Logo sx={{ marginLeft: '10px' }} />

      <Box sx={{ width: '100%', ml: 1 }} />
      {!matchesXs && <Upgrade />}
      {!matchesXs && <FileUploader />}
      {!matchesXs && <Profile />}
      {matchesXs && <MobileSection />}
    </>
  );
};

export default HeaderContent;
