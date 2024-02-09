import { Routes, Route } from "react-router-dom";
import { Toaster } from "sonner";

import HomePage from "./pages/home/HomePage";
import AboutPage from "./pages/home/AboutPage";

import AuthLayout from "./pages/auth/AuthLayout";
import GoogleLoginForm from "./pages/auth/forms/GoogleLoginForm";
import SigninForm from "./pages/auth/forms/SigninForm";
import SignupForm from "./pages/auth/forms/SignupForm";
import VerifyEmail from "./pages/auth/VerifyEmail";

import Documents from "./pages/dashboard/Documents";
import Subscription from "./pages/dashboard/Subscription";

import Chat from "./pages/chat/Chat";
import Share from "./pages/chat/Share";

import "./globals.css";
import DashboardLayout from "./pages/dashboard/DashboardLayout";

const App = () => {
  return (
    <main>
      <Toaster richColors position="top-center" />
      <Routes>
        {/* public routes */}
        <Route index element={<HomePage />} />
        <Route path="/about" element={<AboutPage />} />

        <Route element={<AuthLayout />}>
          <Route path="/google" element={<GoogleLoginForm />} />
          <Route path="/sign-in" element={<SigninForm />} />
          <Route path="/sign-up" element={<SignupForm />} />
          <Route path="/verify-email" element={<VerifyEmail />} />
        </Route>

        {/* private routes */}
        <Route element={<DashboardLayout />}>
          <Route path="/documents" element={<Documents />} />
          <Route path="/subscription" element={<Subscription />} />
          <Route path="/chat" element={<Chat />} />
          <Route path="/share" element={<Share />} />
        </Route>
      </Routes>
    </main>
  );
};

export default App;
