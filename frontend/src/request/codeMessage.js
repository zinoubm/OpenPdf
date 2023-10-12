const codeMessage = {
  200: 'successful Request: The server has successfully returned the requested data.',
  201: 'fulfilled Request: Data has been created or modified successfully.',
  202: 'Accepted: Your request has been queued for processing (asynchronous task).',
  204: 'successful Deletion: Data has been deleted successfully.',
  400: 'Bad request: There was an error in the request, and the server could not create or modify data.',
  401: 'Unauthorized: You do not have permission to access this resource. Please log in again if needed.',
  403: 'Forbidden: You do not have access to this resource, Please check your credentials',
  404: 'Not found: The requested record does not exist, and the server is unable to fulfill the request.',
  406: 'Not acceptable: The requested format is not supported.',
  410: 'Resource deleted: The requested resource has been permanently deleted and is no longer available.',
  422: 'Validation error: When creating an object, a validation error occurred. Please check your input.',
  500: 'Internal server error: Something went wrong on the server. Please contact the server administrator.',
  502: 'Bad gateway: There was an issue with the server gateway. Please try again later.',
  503: 'unavailable Service: The server is currently overloaded or undergoing maintenance. Please try again later.',
  504: 'Gateway timeout: The server gateway has timed out. Please try your request again later.'
};

export default codeMessage;
