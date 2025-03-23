import { format } from "date-fns";
import { useEffect, useRef, useState } from "react";
import LogoutButton from "../components/LogoutButton";
import PostMessage from "../components/PostMessage";
import { BASE_URL } from "../config";
import axiosInstance from "../utils/axiosInstance";

import '../styles/MainPage.css';

const MainPage = () => {
  const [messages, setMessages] = useState([]);
  const [page, setPage] = useState(0);
  const [hasMore, setHasMore] = useState(true);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const messagesContainerRef = useRef(null);
  const limit = 10;

  const fetchMessages = async (pageNum = 0) => {
    try {
      setIsLoading(true);
      const token = localStorage.getItem("access_token");
      const response = await axiosInstance.get(`${BASE_URL}/messages?skip=${pageNum * limit}&limit=${limit}`, {
        headers: { Authorization: `Bearer ${token}` },
      });

      if (pageNum === 0) {
        setMessages(response.data.items.reverse());
      } else {
        setMessages(prev => [...response.data.items.reverse(), ...prev]);
      }

      setHasMore(response.data.has_more);
      setPage(pageNum);
    } catch (err) {
      console.error("Error fetching messages", err);
    } finally {
      setIsLoading(false);
    }
  };


  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const handleScroll = () => {
    if (!messagesContainerRef.current || isLoading || !hasMore) return;

    const { scrollTop } = messagesContainerRef.current;
    if (scrollTop === 0) {
      fetchMessages(page + 1);
    }
  };

  useEffect(() => {
    fetchMessages();
  }, []);

  useEffect(() => {
    if (page === 0) {
      scrollToBottom();
    }
  }, [messages]);

  return (
    <div className="chat-container">
      <div
        className="messages-container"
        ref={messagesContainerRef}
        onScroll={handleScroll}
      >
        <h2>Chat</h2>
        <ul>
          {isLoading && <li className="loading">Loading...</li>}
          {messages.map((msg, index) => (
            <li key={msg.id || index} className="message">
              <strong>{msg.content}</strong>
              <br />
              <small>{format(new Date(msg.created_at), "yyyy-MM-dd HH:mm")}</small>
            </li>
          ))}
        </ul>
        <div ref={messagesEndRef} />
      </div>
      <PostMessage onMessageSent={() => fetchMessages(0)} />
      <LogoutButton />
    </div>
  );
};

export default MainPage;
