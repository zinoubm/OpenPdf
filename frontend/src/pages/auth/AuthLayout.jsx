import { Outlet, Navigate } from "react-router-dom";
import AnimatedCursor from "@/components/shared/AnimatedCursor";
import Logo from "@/components/shared/Logo";

const AuthLayout = () => {
  const isAuthenticated = false;
  return (
    <>
      {isAuthenticated ? (
        <Navigate to="/" />
      ) : (
        <div className="flex h-screen">
          <aside className="hidden p-4 xl:flex xl:flex-col justify-between bg-primary-dark w-2/5 items-center">
            <Logo size={140} theme={"dark"} />

            <h1 className="text-primary-light text-4xl font-bold">
              Some Message, Maybe with a text annimation!{" "}
              <span>
                <AnimatedCursor />
              </span>
            </h1>
            <a className="font-light text-white text-xs">SalesForza, Inc</a>
          </aside>
          <section className="flex flex-1 flex-col items-center justify-center relative">
            <Outlet />
            <img
              className="xl:hidden absolute bottom-4"
              src="/assets/logo-full-light-bg.svg"
              width={140}
            />
          </section>
        </div>
      )}
    </>
  );
};

export default AuthLayout;
