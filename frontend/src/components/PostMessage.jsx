import { useState } from "react";
import axiosInstance from "../utils/axiosInstance";
import { BASE_URL } from "../config";
import '../styles/PostMessage.css';


const PostMessage = ({ onMessageSent }) => {
  const [content, setContent] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (isLoading) return;

    const token = localStorage.getItem("access_token");

    try {
      setIsLoading(true);
      await axiosInstance.post(
        `${BASE_URL}/messages`,
        { content },
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
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="post-message">
      <form onSubmit={handleSubmit}>
        <textarea
          value={content}
          onChange={(e) => setContent(e.target.value)}
          placeholder="How can i help you?"
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading}>
          {isLoading ? "Sending..." : "Send"}
        </button>
      </form>
    </div>
  );
};

export default PostMessage;
