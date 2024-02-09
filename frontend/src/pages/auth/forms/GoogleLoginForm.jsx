import React from "react";
import { GoogleLogin } from "@react-oauth/google";
import { Link } from "react-router-dom";
import { useGoogleSignIn } from "@/lib/api/useAuth";
import { toast } from "sonner";

const GoogleLoginForm = () => {
  const { mutateAsync: SignInGoogle, isPending } = useGoogleSignIn();

  return (
    <div className="flex flex-col items-center">
      <h1 className="font-bold text-2xl m-4">Continue With Google</h1>
      <GoogleLogin
        onSuccess={async (credentialResponse) => {
          SignInGoogle({ token: credentialResponse.credential });
        }}
        onError={() => {
          toast.error("Something Went Wrong, Please Try Again!");
        }}
      />

      {isPending && (
        <span className="p-4">
          <img
            className="animate-spin h-5 w-5 mr-3 inline"
            src="assets/cursor.svg"
          />
        </span>
      )}

      <div className="p-2 font-light text-sm text-slate-600 space-x-2">
        <Link to="/sign-in">Or continue with email</Link>
      </div>
    </div>
  );
};

export default GoogleLoginForm;
