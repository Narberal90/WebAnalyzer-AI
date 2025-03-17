import { useState } from "react";
import axiosInstance from "../utils/axiosInstance";
import { BASE_URL } from "../config";
import '../styles/PostMessage.css';


const PostMessage = ({ onMessageSent }) => {
  const [content, setContent] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    const token = localStorage.getItem("access_token");

    try {
      await axiosInstance.post(
        `${BASE_URL}/messages/message/`,
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
    }
  };

  return (
    <div className="post-message">
      <form onSubmit={handleSubmit}>
        <textarea
          value={content}
          onChange={(e) => setContent(e.target.value)}
          placeholder="How can i help you?"
        />
        <button type="submit">Send</button>
      </form>
    </div>
  );
};

export default PostMessage;
