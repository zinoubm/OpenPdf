import React from 'react';
import { Box, Typography } from '@mui/material';
import { LoadingButton } from '@mui/lab';
import { CloudUploadOutlined } from '@ant-design/icons';
import useApi from 'api/hooks/useApi';
import { useState } from 'react';

import { useDispatch } from 'react-redux';
import { updateRefresKey } from 'store/reducers/app';

function FileUploader() {
  const { uploadDocumentStream } = useApi();
  const dispatch = useDispatch();

  const [isLoading, setIsLoading] = useState(false);

  const handleUpload = ({ target }) => {
    setIsLoading(true);
    uploadDocumentStream(target.files[0]).then(() => {
      setIsLoading(false);
      dispatch(updateRefresKey());
    });
  };

  return (
    <Box>
      <LoadingButton
        size="large"
        variant="contained"
        color="primary"
        sx={{ color: 'black', borderRadius: '10px' }}
        endIcon={<CloudUploadOutlined />}
        component="label"
        loading={isLoading}
        loadingPosition="end"
      >
        <Typography>Upload</Typography>
        <input type="file" onChange={handleUpload} hidden />
      </LoadingButton>
    </Box>
  );
}

export default FileUploader;
