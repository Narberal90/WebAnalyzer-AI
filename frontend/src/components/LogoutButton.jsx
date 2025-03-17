import { useNavigate } from "react-router-dom";
import "../styles/LogoutButton.css";

const LogoutButton = () => {
    const navigate = useNavigate();
  
    const handleLogout = () => {
      localStorage.removeItem("access_token");
      navigate("/");
    };
  
    return (
      <button className="logout-button" onClick={handleLogout}>
        Вийти
      </button>
    );
  };
  
  export default LogoutButton;
  