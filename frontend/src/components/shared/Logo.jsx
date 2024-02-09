import React from "react";
import { Link } from "react-router-dom";

const Logo = ({ className, size, theme }) => {
  return (
    <Link className={className} to="/">
      {theme === "dark" ? (
        <img src="/assets/logo-full-dark-bg.svg" width={size} />
      ) : (
        <img src="/assets/logo-full-light-bg.svg" width={size} />
      )}
    </Link>
  );
};

export default Logo;
