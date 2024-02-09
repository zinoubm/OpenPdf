import React from "react";
import { Link } from "react-router-dom";
import Logo from "@/components/shared/Logo";

const TopBar = () => {
  return (
    <nav className="flex justify-between py-6 px-4 absolute w-full">
      <Logo size={162} />
      <Link
        to="/about"
        className="text-primary-semi-dark xl:text-primary-light xl:mx-12"
      >
        About
      </Link>
    </nav>
  );
};

export default TopBar;
