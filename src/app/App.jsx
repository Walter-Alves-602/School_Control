import { useState } from "react";
import LoginPage from "../pages/login/LoginPage";
import Dashbording from "../pages/dashbording/Dashbording";

function App() {
  const [token, setToken] = useState(() => localStorage.getItem("access_token"));

  function handleLoginSuccess(newToken) {
    localStorage.setItem("access_token", newToken);
    setToken(newToken);
  }

  if (!token) {
    return <LoginPage onLoginSuccess={handleLoginSuccess} />;
  }

  return <Dashbording />;
}

export default App;
