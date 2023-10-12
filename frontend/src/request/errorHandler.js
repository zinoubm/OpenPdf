import { notification } from 'antd';
import codeMessage from './codeMessage';

const errorHandler = (error, status = null) => {
  console.error(error);
  let statusCode;
  if (status) {
    statusCode = error.status;
  } else {
    statusCode = error.response.status;
  }

  notification.config({
    duration: 10
  });
  notification.error({
    message: 'Oops',
    description: codeMessage[statusCode],
    placement: 'bottomRight'
  });

  return { success: false, data: null };
};

export default errorHandler;
