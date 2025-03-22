import { format } from "date-fns";
import { useEffect, useRef, useState } from "react";
import LogoutButton from "../components/LogoutButton";
import PostMessage from "../components/PostMessage";
import { BASE_URL } from "../config";
import axiosInstance from "../utils/axiosInstance";

import '../styles/MainPage.css';

const MainPage = () => {
  const [messages, setMessages] = useState([]);
  const messagesEndRef = useRef(null);

  const fetchMessages = async () => {
    try {
      const token = localStorage.getItem("access_token");
      const response = await axiosInstance.get(`${BASE_URL}/messages`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setMessages(response.data);
    } catch (err) {
      console.error("Error fetching messages", err);
    }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    fetchMessages();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  return (
    <div className="chat-container">
      <div className="messages-container">
        <h2>Chat</h2>
        <ul>
          {messages.map((msg, index) => (
            <li key={index} className="message">
              <strong>{msg.content}</strong>
              <br />
              <small>{format(new Date(msg.created_at), "yyyy-MM-dd HH:mm")}</small>
            </li>
          ))}
        </ul>
        <div ref={messagesEndRef} />
      </div>
      <PostMessage onMessageSent={fetchMessages} />
      <LogoutButton />
    </div>
  );
};

export default MainPage;
