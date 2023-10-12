import { useState, useEffect } from 'react';

import { Menu, Button } from 'antd';
import { FilePdfOutlined, UnorderedListOutlined, DeleteOutlined } from '@ant-design/icons';

import SimpleBar from 'components/third-party/SimpleBar';
import useApi from 'api/hooks/useApi';

import { useSelector, useDispatch } from 'react-redux';
import { activeDocumentId, activeDocumentName, updateRefresKey } from 'store/reducers/app';

const DrawerContent = () => {
  const [documents, setDocuments] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const { getDocuments, deleteDocument } = useApi();
  const dispatch = useDispatch();
  const { refreshKey } = useSelector((state) => state.app);

  const MenuItem = ({ key, documentId, title, children, ...props }) => {
    const handleDeleteDocument = (e) => {
      e.stopPropagation();
      setIsLoading(true);
      deleteDocument(documentId).then(() => {
        setIsLoading(false);
        dispatch(updateRefresKey());
      });
    };
    return (
      <Menu.Item key={key} title={title} style={{ display: 'flex', justifyContent: 'space-between' }} {...props}>
        <Button
          loading={isLoading}
          onClick={handleDeleteDocument}
          danger
          style={{ margin: '1em' }}
          icon={<DeleteOutlined style={{ fontSize: '1em' }} />}
        />
        {children}
      </Menu.Item>
    );
  };

  const handleSelectDocument = (e) => {
    dispatch(activeDocumentId({ documentId: e.key }));
    dispatch(activeDocumentName({ documentName: documents.find((document) => document.id == e.key).title }));
  };

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
      <Menu mode="inline">
        <Menu.SubMenu key={'documents'} title={'Documents'} icon={<FilePdfOutlined />}>
          {documents.map((document) => (
            <MenuItem key={document.id} documentId={document.id} title={document.title} onClick={handleSelectDocument}>
              {document.title}
            </MenuItem>
          ))}
        </Menu.SubMenu>

        <Menu.SubMenu key={'collections'} title={'Collections'} icon={<UnorderedListOutlined />}></Menu.SubMenu>
      </Menu>
    </SimpleBar>
  );
};

export default DrawerContent;
