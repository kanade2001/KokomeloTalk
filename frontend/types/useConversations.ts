import { useCallback, useState } from "react";
import { v4 as uuidv4 } from "uuid";
import { Conversation, MusicConversation } from "./conversation";

const API_URL = "http://localhost:8000";

export const useConversations = () => {
  const [conversations, setConversations] = useState<
    (Conversation | MusicConversation)[]
  >([]);

  const getServerConversation = useCallback(async () => {
    try {
      const response = await fetch(`${API_URL}/conversation/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(conversations),
      });

      if (!response.ok) {
        // サーバーからのレスポンスがエラーだった場合
        throw new Error("Failed to send conversations to the server");
      }

      const data = await response.json();
      console.log("Server response:", data);
      const newConversations = data;
      setConversations((prev) => [
        ...prev,
        { id: uuidv4(), type: "server", text: newConversations },
      ]);
    } catch (error) {
      // サーバーへのリクエストが失敗した場合
      console.error("Error sending conversations to the server:", error);
      setConversations((prev) => [
        ...prev,
        {
          // TODO: Delete
          id: uuidv4(),
          type: "server",
          text: "Failed to send conversations to the server",
        },
        {
          id: uuidv4(),
          type: "system",
          text: "Failed to send conversations to the server",
        },
      ]);
    }
  }, [conversations]);

  const addClientConversation = useCallback(
    (text: string) => {
      setConversations((prev) => [...prev, { id: uuidv4(), type: "client", text }]);
      getServerConversation();
    },
    [getServerConversation]
  );

  return {
    conversations,
    addClientConversation,
    getServerConversation,
  };
};
