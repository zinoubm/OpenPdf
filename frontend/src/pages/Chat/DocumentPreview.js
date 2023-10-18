import React from 'react';
import useApi from 'api/hooks/useApi';
import { useState, useEffect } from 'react';
import { useSelector } from 'react-redux';

function DocumentPreview() {
  const { getDocumentUrl } = useApi();
  const { documentId } = useSelector((state) => state.app);
  const [documentUrl, setDocumentUrl] = useState('');

  useEffect(() => {
    const fetchUrl = async () => {
      if (documentId) {
        const url = await getDocumentUrl(documentId);
        setDocumentUrl(url);
      }
    };

    fetchUrl().catch(console.error);
  }, [documentId]);

  return <iframe style={{ border: 'none', borderRadius: '.8em' }} title="pdf" src={documentUrl} height="110%" width="100%"></iframe>;
}

export default DocumentPreview;
