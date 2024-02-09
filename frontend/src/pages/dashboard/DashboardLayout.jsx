import React, { useState, useEffect, useContext } from "react";
import { isMobile } from "react-device-detect";
import { Outlet, NavLink, useLocation } from "react-router-dom";
import { Toggle } from "@/components/ui/toggle";
import { Button } from "@/components/ui/button";
import { HamburgerMenuIcon } from "@radix-ui/react-icons";
import { Cross1Icon } from "@radix-ui/react-icons";
import Logo from "@/components/shared/Logo";
import AccountManagement from "@/components/shared/AccountManagement";

const SideBarLink = ({ to, label }) => {
  const pathName = useLocation();
  const isActive = pathName.pathname === to;
  return (
    <li>
      <NavLink
        className={`p-3 rounded-md text-black font-normal my-4 px-12  ${
          isActive && " bg-primary-dark text-white "
        } hover:bg-primary-dark hover:text-white`}
        to={to}
      >
        {label}
      </NavLink>
    </li>
  );
};

const DashboardLayout = () => {
  const [isToggle, setisToggle] = useState(!isMobile);

  return (
    <div className="flex">
      {isToggle && (
        <>
          <div className="xl:hidden absolute inset-y-0 z-9999 bg-black opacity-60 h-screen w-screen"></div>
          <div className="transition-all absolute xl:static flex flex-col items-center w-4/5 p-4 xl:w-1/5 inset-y-0 z-9999 bg-white h-screen">
            <span className="flex items-center gap-16">
              <Logo size={162} />
              <Button
                className="p-3 bg-primary-dark hover:bg-primary-light hover:text-primary-dark xl:hidden"
                onClick={() => setisToggle(false)}
              >
                <Cross1Icon width="20" height="20" />
              </Button>
            </span>
            <ul className="flex flex-col items-center gap-6 mt-12">
              <SideBarLink to="/documents" label="Documents" />
              <SideBarLink to="/subscription" label="Subscription" />
            </ul>

            <AccountManagement />
          </div>
        </>
      )}

      <main className="flex-grow">
        <div className="flex items-center justify-between p-2 ">
          <div className="flex items-center space-x-2">
            <Toggle
              onClick={() => {
                setisToggle(!isToggle);
              }}
            >
              <HamburgerMenuIcon width="24" height="24" />
            </Toggle>
            <Logo className="xl:hidden" size={162} />
          </div>
          <Button
            className="bg-primary-dark w-24 hover:bg-primary-light-hover hover:text-primary-dark"
            type="submit"
          >
            Upload
          </Button>
        </div>
        <Outlet />
      </main>
    </div>
  );
};

export default DashboardLayout;
