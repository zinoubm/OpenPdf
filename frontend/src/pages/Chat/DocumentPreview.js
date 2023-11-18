import React from 'react';
import useApi from 'api/hooks/useApi';
import { useState, useEffect } from 'react';
import { useSelector } from 'react-redux';

import { Spin } from 'antd';

function DocumentPreview() {
  const { getDocumentUrl } = useApi();
  const { documentId } = useSelector((state) => state.app);
  const [documentUrl, setDocumentUrl] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const fetchUrl = async () => {
      if (documentId) {
        setIsLoading(true);
        try {
          const url = await getDocumentUrl(documentId);
          setDocumentUrl(url);
        } catch (error) {
          console.error(error);
        } finally {
          setIsLoading(false);
        }
      }
    };

    fetchUrl();
  }, [documentId]);

  return (
    <>
      {isLoading ? (
        <Spin />
      ) : (
        <iframe style={{ border: 'none', borderRadius: '.8em' }} title="pdf" src={documentUrl} height="110%" width="100%"></iframe>
      )}
    </>
  );
}

export default DocumentPreview;
