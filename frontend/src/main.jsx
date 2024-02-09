import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import { GoogleOAuthProvider } from "@react-oauth/google";
import App from "./App";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import AuthProvider from "./context/authContext";

const queryClient = new QueryClient();

ReactDOM.createRoot(document.getElementById("root")).render(
  <GoogleOAuthProvider clientId="351783991998-ct8g6ohg3igm8c4fb2p2kr7igcs8c3tm.apps.googleusercontent.com">
    <BrowserRouter>
      <QueryClientProvider client={queryClient}>
        <AuthProvider>
          <App />
        </AuthProvider>
      </QueryClientProvider>
    </BrowserRouter>
  </GoogleOAuthProvider>
);
