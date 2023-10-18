import logo from 'assets/images/openpdfLogo.svg';

import React from 'react';

const Logo = () => {
  return (
    <div>
      <img src={logo} alt="Logo" style={{ width: '112px', height: 'auto' }} />
    </div>
  );
};

export default Logo;
