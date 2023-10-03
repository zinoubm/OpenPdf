import { FormControl, InputLabel, Select, Typography } from '@mui/material';
import SimpleBar from 'components/third-party/SimpleBar';
import DocumentPicker from './DocumentPicker/index';
import useApi from 'api/hooks/useApi';
import { useState, useEffect } from 'react';

import { useSelector } from 'react-redux';

const DrawerContent = () => {
  const { getDocuments } = useApi();
  const [documents, setDocuments] = useState([]);
  const { documentName, refreshKey } = useSelector((state) => state.app);

  useEffect(() => {
    const fetchDocuments = async () => {
      setDocuments(await getDocuments());
    };

    fetchDocuments();
  }, [refreshKey]);

  return (
    <SimpleBar
      sx={{
        '& .simplebar-content': {
          display: 'flex',
          flexDirection: 'column'
        }
      }}
    >
      <Typography sx={{ color: 'transparent' }}>My Documents</Typography>
      <FormControl fullWidth>
        <InputLabel id="document-picker">Document</InputLabel>
        <Select labelId="document-picker" id="document-selctor" value={documentName} label="Document">
          {documents.map((document, index) => (
            <DocumentPicker key={index} documentId={document.id} documentName={document.title} />
          ))}
        </Select>
      </FormControl>
    </SimpleBar>
  );
};

export default DrawerContent;
