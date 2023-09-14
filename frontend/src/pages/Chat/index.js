import React from 'react';
import ChatBox from './ChatBox';
import DocumentPreview from './DocumentPreview';

import { Grid, useMediaQuery } from '@mui/material';

function Chat() {
  const matchesXs = useMediaQuery((theme) => theme.breakpoints.down('md'));

  return (
    <Grid container spacing={2} sx={{ height: '92%' }}>
      {!matchesXs && (
        <Grid sx={{ height: '100%' }} item xs={6}>
          <DocumentPreview />
        </Grid>
      )}

      <Grid sx={{ height: '100%' }} item xs={matchesXs ? 12 : 6}>
        <ChatBox />
      </Grid>
    </Grid>
  );
}

export default Chat;
