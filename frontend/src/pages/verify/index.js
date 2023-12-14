import React from 'react';
import { Space } from 'antd';
import { useNavigate } from 'react-router-dom';

import './verifyEmail.css';

function VerifyEmail() {
  const navigate = useNavigate();

  return (
    <Space className="verification-container">
      <div className="message">We sent you a Verification Email, Please check your inbox.</div>
      {/* <button
        className="resend-button"
        onClick={() => {
          console.log('Sending verification Email...');
        }}
      >
        Resend Email Verification
      </button> */}
      <button
        className="resend-button"
        onClick={() => {
          navigate('/login');
        }}
      >
        Login
      </button>
    </Space>
  );
}

export default VerifyEmail;
