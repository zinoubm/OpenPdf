import React from 'react';
import { useState, useEffect } from 'react';

import useApi from 'api/hooks/useApi';

import { useSelector, useDispatch } from 'react-redux';
import { updateInputValue } from 'store/reducers/chat';

import { Button, Spin } from 'antd';
import { LoadingOutlined } from '@ant-design/icons';

export const QuestionSuggestions = () => {
  const [suggestions, setSuggestions] = useState([
    'Give a summary of this document',
    'What are the main points discussed in this document?'
  ]);

  const [isLoading, setIsLoading] = useState(false);
  const { documentId } = useSelector((state) => state.app);

  const { getQuestionSuggestions } = useApi();
  const dispatch = useDispatch();

  useEffect(() => {
    console.log('fetching suggestions');
    const fetchQesutionSuggestions = async () => {
      setIsLoading(true);

      const suggestions = await getQuestionSuggestions(documentId);
      setSuggestions(suggestions);

      setIsLoading(false);
    };

    if (documentId) {
      fetchQesutionSuggestions();
    }
  }, [documentId]);

  return (
    <div>
      {isLoading ? (
        <Spin indicator={<LoadingOutlined style={{ fontSize: 24 }} spin />} />
      ) : (
        <ul style={{ listStyle: 'none', padding: 0 }}>
          {suggestions.map((suggestion, index) => (
            <li key={index}>
              <Button
                onClick={() => {
                  dispatch(updateInputValue({ inputValue: suggestion }));
                }}
                style={{ backgroundColor: 'black', color: 'white' }}
                size="large"
              >
                {suggestion}
              </Button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};
