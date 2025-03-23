import { useState } from "react";
import axiosInstance from "../utils/axiosInstance";
import { BASE_URL } from "../config";
import '../styles/PostMessage.css';


const PostMessage = ({ onMessageSent }) => {
  const [content, setContent] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (isLoading) return;

    const trimmedContent = content.trim();
    if (!trimmedContent) {
      setError("Message cannot be empty");
      return;
    }

    const token = localStorage.getItem("access_token");

    try {
      setIsLoading(true);
      setError("");
      await axiosInstance.post(
        `${BASE_URL}/messages`,
        { content: trimmedContent },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      setContent("");
      onMessageSent();
    } catch (error) {
      console.error("Error posting message", error);
      setError("Failed to send message. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="post-message">
      <form onSubmit={handleSubmit}>
        <textarea
          value={content}
          onChange={(e) => {
            setContent(e.target.value);
            setError("");
          }}
          placeholder="How can i help you?"
          disabled={isLoading}
        />
        {error && <p className="error-message">{error}</p>}
        <button 
          type="submit" 
          disabled={isLoading}
        >
          {isLoading ? "Sending..." : "Send"}
        </button>
      </form>
    </div>
  );
};

export default PostMessage;
