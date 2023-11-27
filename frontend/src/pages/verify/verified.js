import React from 'react';
import { Space } from 'antd';

import './verifyEmail.css';

function verified() {
  return (
    <Space className="verification-container">
      <h1>Email Verified Successfully, You Can close this page.</h1>
    </Space>
  );
}

export default verified;
