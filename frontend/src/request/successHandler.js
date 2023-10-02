import { notification } from 'antd';

import codeMessage from './codeMessage';

const successHandler = (response, options = { notifyOnSuccess: false, notifyOnFailed: true }) => {
  const { data } = response;

  if (data) {
    if (options.notifyOnSuccess) {
      notification.config({
        duration: 5
      });
      notification.success({
        message: `Request success`,
        description: successText
      });

      return data;
    }
  }

  const errorText = codeMessage[response.status];

  const { status } = response;

  if (options.notifyOnFailed) {
    notification.config({
      duration: 5
    });
    notification.error({
      message: `Request error ${status}`,
      description: errorText
    });
  }

  return null;
};

export default successHandler;
