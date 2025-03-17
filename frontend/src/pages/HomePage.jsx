import { Link } from "react-router-dom";
import '../styles/HomePage.css';


const HomePage = () => {
  return (
    <div className="home-container">
      <h1>Welcome to the Chat App</h1>
      <div className="buttons">
        <Link to="/login">
          <button>Login</button>
        </Link>
        <Link to="/register">
          <button>Register</button>
        </Link>
      </div>
    </div>
  );
};

export default HomePage;
