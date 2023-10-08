import { notification } from 'antd';

import codeMessage from './codeMessage';

const successHandler = (response, options = { notifyOnSuccess: false, notifyOnFailed: true }) => {
  const { data, status } = response;
  const message = codeMessage[status];
  if (data) {
    if (options.notifyOnSuccess) {
      notification.config({
        duration: 5
      });
      notification.success({
        message: `Request success`,
        description: message,
        placement: 'bottomLeft'
      });
    }
    return { success: true, data: data };
  }

  if (options.notifyOnFailed) {
    notification.config({
      duration: 5
    });
    notification.error({
      message: `Request error ${status}`,
      description: message,
      placement: 'bottomLeft'
    });
  }

  return { success: false, data: null };
};

export default successHandler;
