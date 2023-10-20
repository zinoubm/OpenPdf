import React from 'react';
import { useState, useEffect, useRef } from 'react';

import { List, Input, Space, Button, Alert, Typography, Card } from 'antd';
import { UserOutlined } from '@ant-design/icons';

import useApi from 'api/hooks/useApi';
import { useSelector, useDispatch } from 'react-redux';
import { updateIsLoading } from 'store/reducers/chat';

import Markdown from 'react-markdown';

import miniLogo from 'assets/images/miniLogo.svg';
import './scrollBar.css';

const { Title } = Typography;

const questionSuggestions = ['Give a summary of this document', 'What are the main points discussed in this document?'];

const ChatBox = () => {
  const { queryDocument } = useApi();
  const dispatch = useDispatch();

  const { messages, isLoading } = useSelector((state) => state.chat);
  const { documentName, documentId } = useSelector((state) => state.app);

  const [inputValue, setInputValue] = useState('');
  const [isAlert, setisAlert] = useState(false);

  const listRef = useRef();
  const messageInput = useRef();

  const defaultMessage = [
    { entity: 'bot', message: 'Hello, feel free to check out these examples 😎.' },
    {
      entity: 'bot',
      message: (
        <Space direction="vertical">
          {questionSuggestions.map((suggestion, index) => {
            return (
              <Button
                key={index}
                value={suggestion}
                style={{ width: '100%', border: '1px black solid' }}
                onClick={() => {
                  setInputValue(suggestion);
                }}
              >
                {suggestion}
              </Button>
            );
          })}
        </Space>
      )
    }
  ];

  const handleSubmit = async () => {
    if (documentId === null) {
      setisAlert(true);
      return;
    } else {
      setisAlert(false);
    }
    const currentMessage = messageInput.current.input.value;
    dispatch(updateIsLoading({ isLoading: true }));
    setInputValue('');
    await queryDocument(currentMessage, documentId);
  };

  const handleInputChange = (e) => {
    setInputValue(e.target.value);
  };

  useEffect(() => {
    if (listRef.current) {
      listRef.current.scrollTop = listRef.current.scrollHeight;
    }
  }, [messages]);

  return (
    <Card
      title={
        <Title level={3} ellipsis>
          {documentName}
        </Title>
      }
    >
      {isAlert && <Alert style={{ position: 'absolute' }} message="Please, Select a document!" type="error" />}

      <List
        style={{ padding: '2em', overflowY: 'auto', height: '65vh' }}
        itemLayout="vertical"
        className="custom-scrollbar"
        dataSource={messages.length > 0 ? messages : defaultMessage}
        ref={listRef}
        renderItem={(item) => (
          <List.Item style={{ padding: '1em' }}>
            {item.entity === 'user' ? (
              <UserOutlined
                style={{
                  marginRight: '1em',
                  fontSize: '1.4em'
                }}
              />
            ) : (
              <img
                src={miniLogo}
                alt="entity"
                style={{
                  width: '1.6em',
                  height: 'auto',
                  marginRight: '1em'
                }}
              />
            )}
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
        <Button loading={isLoading} style={{ background: '#0a0a0a', height: '100%' }} type="primary" onClick={handleSubmit}>
          Send
        </Button>
      </Space.Compact>
    </Card>
  );
};

export default ChatBox;
