// ==============================|| PRESET THEME - THEME SELECTOR ||============================== //

const Theme = (colors) => {
  const { primaryColor, orangeAccentColor, blueAccentColor, cyanAccentColor, red, gold, cyan, green, grey } = colors;
  const greyColors = {
    0: grey[0],
    50: grey[1],
    100: grey[2],
    200: grey[3],
    300: grey[4],
    400: grey[5],
    500: grey[6],
    600: grey[7],
    700: grey[8],
    800: grey[9],
    900: grey[10],
    A50: grey[15],
    A100: grey[11],
    A200: grey[12],
    A400: grey[13],
    A700: grey[14],
    A800: grey[16]
  };
  const contrastText = '#fff';
  const darkContrastText = '#000';

  return {
    primary: {
      lighter: primaryColor[0],
      100: primaryColor[1],
      200: primaryColor[2],
      light: primaryColor[3],
      400: primaryColor[4],
      main: primaryColor[5],
      dark: primaryColor[6],
      700: primaryColor[7],
      darker: primaryColor[8],
      900: primaryColor[9],
      contrastText
    },
    orangeAccent: {
      lighter: orangeAccentColor[0],
      100: orangeAccentColor[1],
      200: orangeAccentColor[2],
      light: orangeAccentColor[3],
      400: orangeAccentColor[4],
      main: orangeAccentColor[5],
      dark: orangeAccentColor[6],
      700: orangeAccentColor[7],
      darker: orangeAccentColor[8],
      900: orangeAccentColor[9],
      contrastText: greyColors[0]
    },
    blueAccent: {
      lighter: blueAccentColor[0],
      100: blueAccentColor[1],
      200: blueAccentColor[2],
      light: blueAccentColor[3],
      400: blueAccentColor[4],
      main: blueAccentColor[5],
      dark: blueAccentColor[6],
      700: blueAccentColor[7],
      darker: blueAccentColor[8],
      900: blueAccentColor[9],
      contrastText: greyColors[0]
    },
    cyanAccent: {
      lighter: cyanAccentColor[0],
      100: cyanAccentColor[1],
      200: cyanAccentColor[2],
      light: cyanAccentColor[3],
      400: cyanAccentColor[4],
      main: cyanAccentColor[5],
      dark: cyanAccentColor[6],
      700: cyanAccentColor[7],
      darker: cyanAccentColor[8],
      900: cyanAccentColor[9],
      contrastText: darkContrastText
    },
    secondary: {
      lighter: greyColors[100],
      100: greyColors[100],
      200: greyColors[200],
      light: greyColors[300],
      400: greyColors[400],
      main: greyColors[500],
      600: greyColors[600],
      dark: greyColors[700],
      800: greyColors[800],
      darker: greyColors[900],
      A100: greyColors[0],
      A200: greyColors.A400,
      A300: greyColors.A700,
      contrastText: greyColors[0]
    },
    error: {
      lighter: red[0],
      light: red[2],
      main: red[4],
      dark: red[7],
      darker: red[9],
      contrastText
    },
    warning: {
      lighter: gold[0],
      light: gold[3],
      main: gold[5],
      dark: gold[7],
      darker: gold[9],
      contrastText: greyColors[100]
    },
    info: {
      lighter: cyan[0],
      light: cyan[3],
      main: cyan[5],
      dark: cyan[7],
      darker: cyan[9],
      contrastText
    },
    success: {
      lighter: green[0],
      light: green[3],
      main: green[5],
      dark: green[7],
      darker: green[9],
      contrastText
    },
    grey: greyColors
  };
};

export default Theme;
