import React from 'react';
import { Box, Typography } from '@mui/material';
import { LoadingButton } from '@mui/lab';

import { CloudUploadOutlined } from '@ant-design/icons';
import useApi from 'api/hooks/useApi';
import { useState } from 'react';

import { useDispatch } from 'react-redux';
import { activeDocumentId, activeDocumentName, updateRefresKey, activeSelectedKeys } from 'store/reducers/app';

function FileUploader() {
  const { uploadDocumentStream, uploadDocument } = useApi();
  const dispatch = useDispatch();

  const [isLoading, setIsLoading] = useState(false);

  const handleUpload = async ({ target }) => {
    setIsLoading(true);
    try {
      let response;
      if (process.env.REACT_APP_ENVIRONMENT === 'prod') {
        response = await uploadDocumentStream(target.files[0]);
      } else {
        response = await uploadDocument(target.files[0]);
      }

      dispatch(activeDocumentId({ documentId: response.data.document_id }));
      dispatch(activeDocumentName({ documentName: response.data.document_title }));
      dispatch(activeSelectedKeys({ selectedKeys: null }));
      dispatch(updateRefresKey());
    } catch (error) {
      // console.error('Error occurred during upload:', error);
      if (error.status === 402) {
        notification.config({
          duration: 10
        });

        notification.info({
          message: `Plan Limits Reached.`,
          description: 'You reached your subscription limits, Please Upgrade to get more quotas.',
          placement: 'bottomRight'
        });
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Box>
      <LoadingButton
        size="large"
        variant="contained"
        sx={{ color: 'black', borderRadius: '10px', background: 'transparent', border: 'solid 2px' }}
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
