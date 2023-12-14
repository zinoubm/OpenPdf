import React from 'react';
import { Upload, message } from 'antd';
// import { Upload } from 'antd';
import { InboxOutlined } from '@ant-design/icons';
import useApi from 'api/hooks/useApi';

import { useDispatch } from 'react-redux';
import { activeDocumentId, activeDocumentName, updateRefresKey, activeSelectedKeys } from 'store/reducers/app';

const { Dragger } = Upload;

const DocumentUploadArea = () => {
  const { uploadDocumentStream } = useApi();
  const dispatch = useDispatch();

  const props = {
    name: 'file',
    multiple: true,
    action: null,

    onChange(info) {
      const { status } = info.file;
      if (status !== 'uploading') {
        console.log(info.file, info.fileList);
      }
      if (status === 'done') {
        message.success(`${info.file.name} file uploaded successfully.`);
      } else if (status === 'error') {
        message.error(`${info.file.name} file upload failed.`);
      }
    },

    async onDrop(e) {
      console.log('Dropped files', e.dataTransfer.files);
      console.log('e', e);

      if (e.dataTransfer.files.lenght === 1) {
        console.log('uploading');
        const response = await uploadDocumentStream(e.dataTransfer.files[0]);

        dispatch(activeDocumentId({ documentId: response.data.document_id }));
        dispatch(activeDocumentName({ documentName: response.data.document_title }));
        dispatch(activeSelectedKeys({ selectedKeys: null }));
        dispatch(updateRefresKey());

        console.log('finished');
      }
    }
  };

  // const onChange = () => {
  //   console.log('info from change', info);
  //   const { status } = info.file;
  //   if (status !== 'uploading') {
  //     console.log(info.file, info.fileList);
  //   }
  //   if (status === 'done') {
  //     message.success(`${info.file.name} file uploaded successfully.`);
  //   } else if (status === 'error') {
  //     message.error(`${info.file.name} file upload failed.`);
  //   }
  // };

  // const onDrop = async (e) => {
  //   console.log('Dropped files', e.dataTransfer.files);
  //   console.log('e', e);

  //   if (e.dataTransfer.files.lenght === 100) {
  //     const response = await uploadDocumentStream(e.dataTransfer.files[0]);

  //     dispatch(activeDocumentId({ documentId: response.data.document_id }));
  //     dispatch(activeDocumentName({ documentName: response.data.document_title }));
  //     dispatch(activeSelectedKeys({ selectedKeys: null }));
  //     dispatch(updateRefresKey());
  //   }
  // };
  return (
    <Dragger
      // name="file"
      // // action="https://run.mocky.io/v3/435e224c-44fb-4773-9faf-380c5e6a2188"
      // multiple={false}
      // onChange={onChange}
      // onDrop={onDrop}
      {...props}
    >
      <p className="ant-upload-drag-icon">
        <InboxOutlined />
      </p>
      <p className="ant-upload-text">Click or drag file to this area to upload</p>
    </Dragger>
  );
};

export default DocumentUploadArea;
