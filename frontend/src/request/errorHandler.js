import { notification } from 'antd';
import navigate from '@/utils/navigate';
import codeMessage from './codeMessage';

const errorHandler = (error) => {
  const { response } = error;

  if (response && response.status) {
    const { data, status } = response;

    const errorText = codeMessage[status];

    notification.config({
      duration: 10
    });
    notification.error({
      message: `Request error ${status}`,
      description: errorText
    });

    if (status == 403) {
      navigate('/login');
    }
    return data;
  }

  notification.config({
    duration: 5
  });
  notification.error({
    message: 'No internet connection',
    description: 'Cannot connect to the server, Check your internet network'
  });

  return {
    success: false,
    result: null,
    message: 'Cannot connect to the server, Check your internet network'
  };
};

export default errorHandler;
