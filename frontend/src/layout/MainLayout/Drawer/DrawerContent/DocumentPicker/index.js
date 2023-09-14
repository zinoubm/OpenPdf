import React from 'react';
import { Stack, MenuItem, Card } from '@mui/material';
import { Button } from '@mui/material';
import { DeleteOutlined } from '@ant-design/icons';
import { useDispatch } from 'react-redux';
import useApi from 'api/hooks/useApi';
import { activeDocumentId, activeDocumentName } from 'store/reducers/app';

const DocumentPicker = ({ documentName, documentId }) => {
  const { deleteDocument } = useApi();
  const dispatch = useDispatch();

  return (
    <Card sx={{ padding: '5px', borderRadius: '10px' }} variant="outlined">
      <Stack spacing={2} direction="row">
        <MenuItem
          value={documentName}
          onClick={() => {
            dispatch(activeDocumentId({ documentId: documentId }));
            dispatch(activeDocumentName({ documentName: documentName }));
          }}
        >
          {documentName}
        </MenuItem>
        <Button
          onClick={() => {
            deleteDocument(documentId);
          }}
          color="secondary"
          size={'50px'}
          startIcon={<DeleteOutlined />}
        />
      </Stack>
    </Card>
  );
};

export default DocumentPicker;
