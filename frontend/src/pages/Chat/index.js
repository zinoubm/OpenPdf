import React from 'react';
import ChatBox from './ChatBox';
import DocumentPreview from './DocumentPreview';
// import DocumentUploadArea from './DocumentUploadArea';
import { DocumentTimeline } from './DocumentTimeline';

import { useSelector } from 'react-redux';

import { Grid, useMediaQuery } from '@mui/material';

function Chat() {
  const matchesXs = useMediaQuery((theme) => theme.breakpoints.down('md'));
  const { documentId } = useSelector((state) => state.app);

  return (
    <Grid container spacing={2} sx={{ height: '92%' }}>
      {!matchesXs && (
        <Grid sx={{ height: '100%', width: '100%' }} item xs={6}>
          {documentId ? <DocumentPreview /> : <DocumentTimeline />}
        </Grid>
      )}

      {/* {!matchesXs && (
        <Grid sx={{ height: '100%' }} item xs={6}>
          <DocumentPreview />
        </Grid>
      )} */}

      <Grid sx={{ height: '100%' }} item xs={matchesXs ? 12 : 6}>
        <ChatBox />
      </Grid>
    </Grid>
  );
}

export default Chat;
