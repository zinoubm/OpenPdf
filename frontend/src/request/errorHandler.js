import { notification } from 'antd';

const errorHandler = (error) => {
  console.log(error);

  notification.config({
    duration: 10
  });
  notification.error({
    message: 'Oops',
    description: 'Something Went Wrong, Please Refresh and Retry Again',
    placement: 'bottomLeft'
  });

  return { success: false, data: null };
};

export default errorHandler;
