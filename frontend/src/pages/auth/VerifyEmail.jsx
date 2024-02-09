import React from "react";
import { Button } from "@/components/ui/button";
import { Link } from "react-router-dom";

const VerifyEmail = () => {
  return (
    <div className="flex flex-col items-center text-center">
      <h1 className="font-bold text-2xl">
        We sent you a Verification Email, Please check your inbox.
      </h1>
      <Button
        asChild
        className="bg-primary-light text-primary-dark font-normal w-36 my-4 px-12 hover:bg-primary-light-hover"
      >
        <Link to="/sign-in">Sign In</Link>
      </Button>
    </div>
  );
};

export default VerifyEmail;
