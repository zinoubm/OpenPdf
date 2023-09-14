// material-ui
// import { Box, IconButton, Link, useMediaQuery } from '@mui/material';
// import { useMediaQuery } from '@mui/material';
import { Box, Chip, useMediaQuery } from '@mui/material';
import Logo from 'components/Logo';
// import { GithubOutlined } from '@ant-design/icons';
import FileUploader from './FileUploader/index';
// project import
// import Search from './Search';
import Profile from './Profile';
// import Notification from './Notification';
import MobileSection from './MobileSection';

// ==============================|| HEADER - CONTENT ||============================== //

const HeaderContent = () => {
  const matchesXs = useMediaQuery((theme) => theme.breakpoints.down('md'));

  return (
    <>
      {/* {!matchesXs && <Search />} */}
      {/* {matchesXs && <Box sx={{ width: '100%', ml: 1 }} />} */}
      <Logo sx={{ marginLeft: '10px' }} />
      <Chip
        label={process.env.REACT_APP_VERSION}
        size="small"
        sx={{ height: 16, marginLeft: '10px', '& .MuiChip-label': { fontSize: '0.625rem', py: 0.25 } }}
        component="a"
        href="https://github.com/codedthemes/mantis-free-react-admin-template"
        target="_blank"
        clickable
      />
      <Box sx={{ width: '100%', ml: 1 }} />

      {/* <IconButton
        component={Link}
        href="https://github.com/codedthemes/mantis-free-react-admin-template"
        target="_blank"
        disableRipple
        color="secondary"
        title="Download Free Version"
        sx={{ color: 'text.primary', bgcolor: 'grey.100' }}
      >
        <GithubOutlined />
      </IconButton> */}

      {/* <Notification /> */}
      {!matchesXs && <FileUploader />}
      {!matchesXs && <Profile />}
      {matchesXs && <MobileSection />}
    </>
  );
};

export default HeaderContent;
