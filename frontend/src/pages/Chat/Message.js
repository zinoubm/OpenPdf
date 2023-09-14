import React from 'react';
import { Typography } from '@mui/material';

const Message = ({ message }) => {
  return (
    <Typography sx={{ background: '#99DBF5', padding: '.8em', borderRadius: '15px 15px 15px 5px', width: '75%' }}>{message}</Typography>
  );
};

export default Message;
