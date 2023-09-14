import React from 'react';
import { Box, Typography } from '@mui/material';
import { LoadingButton } from '@mui/lab';
import { CloudUploadOutlined } from '@ant-design/icons';
import useUploadFile from 'api/hooks/useUploadFile';
import { useState } from 'react';

function FileUploader() {
  const uploadFile = useUploadFile();
  const [isLoading, setIsLoading] = useState(false);

  const handleUpload = ({ target }) => {
    setIsLoading(true);
    uploadFile(target.files[0]).then((res) => {
      console.log(res);
      setIsLoading(false);
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
