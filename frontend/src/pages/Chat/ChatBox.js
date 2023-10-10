import React from 'react';
import { useState, useEffect, useRef } from 'react';
import { List, Input, Space, Button, Alert } from 'antd';
import { useSelector } from 'react-redux';
import miniLogo from 'assets/images/miniLogo.svg';
import { Paper, Typography } from '@mui/material';
import { UserOutlined } from '@ant-design/icons';
import useApi from 'api/hooks/useApi';
import './scrollBar.css';

const defaultMessage = [
  {
    entity: 'bot',
    message:
      'Hey there, you can try something like: "Give a summary of this document" or "What are the main points discussed in this document?"'
  }
];

const ChatBox = () => {
  const { queryDocument } = useApi();
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isAlert, setisAlert] = useState(false);
  const listRef = useRef();
  const messageInput = useRef();
  const { documentName, documentId } = useSelector((state) => state.app);

  const handleSubmit = () => {
    if (documentId === null) {
      setisAlert(true);
      return;
    } else {
      setisAlert(false);
    }

    setNewMessage(messageInput.current.input.value);
    setInputValue('');
    setIsLoading(true);
    setMessages([...messages, { entity: 'user', message: messageInput.current.input.value }]);
  };

  const handleInputChange = (e) => {
    setInputValue(e.target.value);
  };

  useEffect(() => {
    if (listRef.current) {
      listRef.current.scrollTop = listRef.current.scrollHeight;
    }
  }, [messages]);

  useEffect(() => {
    queryDocument(newMessage, documentId, messages, setMessages, setIsLoading);
  }, [newMessage]);

  return (
    <Paper
      title={documentName}
      style={{
        padding: '1em',
        height: '100%',
        boxShadow: '0 0px 0px #333',
        border: '1px #ededed solid'
      }}
    >
      <Typography variant="h4">{documentName}</Typography>
      {isAlert && <Alert style={{ position: 'absolute' }} message="Please, Select a document!" type="error" />}
      <List
        style={{ padding: '2em', overflowY: 'auto', height: '85%' }}
        itemLayout="horizontal"
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
                  width: '1em',
                  height: 'auto',
                  marginRight: '1em'
                }}
              />
            )}
            {item.message}
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
        <Button loading={isLoading} style={{ background: '#FEC61E', height: '100%' }} type="primary" onClick={handleSubmit}>
          Send
        </Button>
      </Space.Compact>
    </Paper>
  );
};

export default ChatBox;
