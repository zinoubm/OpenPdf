import React from 'react';
import { useState, useEffect, useRef } from 'react';

import { List, Spin, Input, Space, Button, Alert, Typography, Card, Popover } from 'antd';

import useApi from 'api/hooks/useApi';
import { useSelector, useDispatch } from 'react-redux';
import { updateMessages, updateIsLoading, updateInputValue } from 'store/reducers/chat';

import { QuestionSuggestions } from './QuestionSuggestions';

import Markdown from 'react-markdown';

import { BulbOutlined } from '@ant-design/icons';

import miniLogo from 'assets/images/miniLogo.svg';
import './scrollBar.css';

const { Title } = Typography;

const ChatBox = () => {
  const { queryDocument, getDocumentStatus } = useApi();
  const dispatch = useDispatch();

  const { messages, inputValue, isLoading } = useSelector((state) => state.chat);
  const [isDocumentLoading, setIsDocumentLoading] = useState(false);
  const { userFullName } = useSelector((state) => state.auth);
  const { documentName, documentId } = useSelector((state) => state.app);

  const [isAlert, setisAlert] = useState(false);
  const [isSuggestionsOpen, setIsSuggestionsOpen] = useState(false);

  const messageInput = useRef();

  const defaultMessage = [{ entity: 'system', message: 'Hello, How can we help you today?' }];

  const handleSuggest = async () => {
    setIsSuggestionsOpen(!isSuggestionsOpen);
  };

  const handleSubmit = async () => {
    if (documentId === null) {
      setisAlert(true);
      return;
    } else {
      setisAlert(false);
    }
    const currentMessage = messageInput.current.input.value;
    dispatch(updateIsLoading({ isLoading: true }));
    dispatch(updateInputValue({ inputValue: '' }));

    dispatch(updateMessages({ messages: { entity: 'user', message: currentMessage }, accumulate: false }));
    await queryDocument(currentMessage, messages, documentId);
  };

  const handleInputChange = (e) => {
    dispatch(updateInputValue({ inputValue: e.target.value }));
  };

  let intervalId;
  const checkDocumentStatus = async () => {
    try {
      if (documentId) {
        const status = await getDocumentStatus(documentId);

        if (status === true) {
          setIsDocumentLoading(false);
          clearInterval(intervalId);
        }
      }
    } catch (error) {
      console.error('Error checking document status:', error);
    }
  };

  useEffect(() => {
    if (documentId) {
      setIsDocumentLoading(true);
    }

    intervalId = setInterval(checkDocumentStatus, 1000);
  }, [documentId]);

  useEffect(() => {
    if (isSuggestionsOpen === false && documentId != null) setIsSuggestionsOpen(true);
  }, [documentId]);

  return (
    <Card
      style={{ height: '100%' }}
      title={
        <Title level={3} ellipsis>
          {documentName}
        </Title>
      }
    >
      {isAlert && <Alert style={{ position: 'absolute' }} message="Please, Select a document!" type="error" />}

      {isDocumentLoading ? (
        <div style={{ height: '40vh', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
          <Spin />
        </div>
      ) : (
        <>
          <List
            style={{ padding: '2em', overflowY: 'auto', height: '65vh' }}
            itemLayout="vertical"
            className="custom-scrollbar"
            dataSource={messages.length > 0 ? messages : defaultMessage}
            renderItem={(item) => (
              <List.Item style={{ padding: '1em' }}>
                {item.entity === 'user' ? (
                  <div style={{ display: 'flex', alignItems: 'center' }}>
                    <div
                      style={{
                        backgroundColor: '#0a0a0a',
                        width: '36px',
                        height: '36px',
                        borderRadius: '50%',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        color: 'white',
                        fontWeight: 'bold',
                        fontSize: '20px',
                        marginRight: '1em'
                      }}
                    >
                      {userFullName[0].toUpperCase()}
                    </div>
                    <Title level={5}>You</Title>
                  </div>
                ) : (
                  <div style={{ display: 'flex', alignItems: 'center' }}>
                    <img
                      src={miniLogo}
                      alt="entity"
                      style={{
                        width: '1.6em',
                        height: 'auto',
                        marginRight: '1em'
                      }}
                    />
                    <Title level={5}>OpenPdfAI</Title>
                  </div>
                )}
                <br />
                {messages.length > 0 ? <Markdown>{item.message.trim()}</Markdown> : item.message}
              </List.Item>
            )}
          />

          <Space.Compact style={{ height: '3em', width: '100%' }}>
            <Input
              value={inputValue}
              onChange={handleInputChange}
              onPressEnter={handleSubmit}
              placeholder="Ask a question"
              ref={messageInput}
            />

            <Popover content={<QuestionSuggestions />} open={isSuggestionsOpen} placement="topRight" title="Suggestions">
              <Button style={{ background: 'transparent', height: '100%', color: '#0ec295' }} onClick={handleSuggest}>
                <BulbOutlined />
              </Button>
            </Popover>

            <Button loading={isLoading} style={{ background: '#0a0a0a', height: '100%' }} type="primary" onClick={handleSubmit}>
              Send
            </Button>
          </Space.Compact>
        </>
      )}
    </Card>
  );
};

export default ChatBox;
