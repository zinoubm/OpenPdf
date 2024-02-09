import { useState, useEffect, createContext } from "react";
import { useNavigate } from "react-router-dom";
import { useCurrentUser } from "@/lib/api/useAuth";

export const AuthContext = createContext(undefined);

// for multiple providers wrap them toghether in an app context and use it with top level components (main)
const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(undefined);
  const { mutateAsync: getCurrentUser, isPending } = useCurrentUser();

  useEffect(() => {
    const updateCurrentUser = async () => {
      const currentUser = await getCurrentUser();
      setUser(currentUser);
    };
    updateCurrentUser();
  }, []);

  return (
    <AuthContext.Provider value={{ user, setUser }}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthProvider;
