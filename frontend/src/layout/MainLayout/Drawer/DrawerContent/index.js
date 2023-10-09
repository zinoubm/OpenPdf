import { useState, useEffect } from 'react';

import { Menu } from 'antd';
import { FilePdfOutlined, UnorderedListOutlined } from '@ant-design/icons';
import { FormControl, InputLabel, Select, Typography } from '@mui/material';

import SimpleBar from 'components/third-party/SimpleBar';
import DocumentPicker from './DocumentPicker/index';
import useApi from 'api/hooks/useApi';

import { useSelector, useDispatch } from 'react-redux';
import { activeDocumentId, activeDocumentName } from 'store/reducers/app';

function getItem(label, key, icon, children, type) {
  return {
    key,
    icon,
    children,
    label,
    type
  };
}

const DrawerContent = () => {
  const [documents, setDocuments] = useState([]);
  const [menuItems, setMenuItems] = useState([]);

  const { getDocuments } = useApi();

  const dispatch = useDispatch();
  const { documentName, refreshKey } = useSelector((state) => state.app);

  const handleSelectDocument = (e) => {
    dispatch(activeDocumentId({ documentId: e.key }));
    dispatch(activeDocumentName({ documentName: documents.find((document) => document.id == e.key).title }));
  };

  useEffect(() => {
    const itemsDocumentsList = documents.map((document) => getItem(document.title, document.id));
    const items = [
      getItem('Documents', 'documents-sub', <FilePdfOutlined />, itemsDocumentsList),
      getItem('Collections', 'collections-sub', <UnorderedListOutlined />, []),
      {
        type: 'divider'
      }
    ];
    setMenuItems(items);
  }, [documents]);

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

      <Menu
        onClick={handleSelectDocument}
        style={{
          width: 256
        }}
        defaultOpenKeys={['documents-sub']}
        mode="inline"
        items={menuItems}
      />
    </SimpleBar>
  );
};

export default DrawerContent;
