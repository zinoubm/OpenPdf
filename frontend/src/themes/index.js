import PropTypes from 'prop-types';
import { useMemo } from 'react';

// material-ui
import { CssBaseline, StyledEngineProvider } from '@mui/material';
import { createTheme, ThemeProvider } from '@mui/material/styles';

// project import
import Palette from './palette';
import Typography from './typography';
import CustomShadows from './shadows';
import componentsOverride from './overrides';

// ==============================|| DEFAULT THEME - MAIN  ||============================== //

export default function ThemeCustomization({ children }) {
  const theme = Palette('light', 'default');

  // eslint-disable-next-line react-hooks/exhaustive-deps
  const themeTypography = Typography(`'Public Sans', sans-serif`);
  const themeCustomShadows = useMemo(() => CustomShadows(theme), [theme]);

  const themeOptions = useMemo(
    () => ({
      breakpoints: {
        values: {
          xs: 0,
          sm: 768,
          md: 1024,
          lg: 1266,
          xl: 1536
        }
      },
      direction: 'ltr',
      mixins: {
        toolbar: {
          minHeight: 60,
          paddingTop: 8,
          paddingBottom: 8
        }
      },
      palette: theme.palette,
      customShadows: themeCustomShadows,
      typography: themeTypography
      // ,components: {
      //   MuiCssBaseline: {
      //     styleOverrides: {
      //       body: {
      //         scrollbarColor: '#6b6b6b #2b2b2b',
      //         '&::-webkit-scrollbar, & *::-webkit-scrollbar': {
      //           backgroundColor: '#2b2b2b'
      //         },
      //         '&::-webkit-scrollbar-thumb, & *::-webkit-scrollbar-thumb': {
      //           borderRadius: 8,
      //           backgroundColor: '#6b6b6b',
      //           minHeight: 24,
      //           border: '3px solid #2b2b2b'
      //         },
      //         '&::-webkit-scrollbar-thumb:focus, & *::-webkit-scrollbar-thumb:focus': {
      //           backgroundColor: '#959595'
      //         },
      //         '&::-webkit-scrollbar-thumb:active, & *::-webkit-scrollbar-thumb:active': {
      //           backgroundColor: '#959595'
      //         },
      //         '&::-webkit-scrollbar-thumb:hover, & *::-webkit-scrollbar-thumb:hover': {
      //           backgroundColor: '#959595'
      //         },
      //         '&::-webkit-scrollbar-corner, & *::-webkit-scrollbar-corner': {
      //           backgroundColor: '#2b2b2b'
      //         }
      //       }
      //     }
      //   }
      // }
    }),
    [theme, themeTypography, themeCustomShadows]
  );

  const themes = createTheme(themeOptions);
  themes.components = componentsOverride(themes);

  return (
    <StyledEngineProvider injectFirst>
      <ThemeProvider theme={themes}>
        <CssBaseline />
        {children}
      </ThemeProvider>
    </StyledEngineProvider>
  );
}

ThemeCustomization.propTypes = {
  children: PropTypes.node
};
