import React from "react";
import AnimatedCursor from "@/components/shared/AnimatedCursor";
import { Button } from "@/components/ui/button";
import { Link } from "react-router-dom";

const Hero = () => {
  return (
    <>
      <div className="flex h-screen">
        <div className="flex flex-col justify-center xl:w-2/5  py-24 px-5">
          <h1 className="h1-bold text-primary-semi-dark">
            Chat with Documents. Read 64% Faster!{" "}
            <span>
              <AnimatedCursor />
            </span>
          </h1>
          <p className="text-primary-semi-dark text-xl mt-8">
            Ea cupidatat proident nulla dolore duis mollit exercitation.
          </p>
          <Button
            asChild
            className="bg-primary-light text-primary-dark font-normal w-36 my-4 px-12 hover:bg-primary-light-hover"
          >
            <Link to="/google">Get Started</Link>
          </Button>
        </div>
        <div className="flex-grow bg-primary-dark hidden xl:flex">
          <p>Drop A Pdf</p>
        </div>
      </div>
    </>
  );
};

export default Hero;
