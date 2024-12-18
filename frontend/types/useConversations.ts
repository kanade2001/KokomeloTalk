import { useCallback, useState } from "react";
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
        { id: "id", type: "server", text: newConversations },
      ]);
    } catch (error) {
      // サーバーへのリクエストが失敗した場合
      console.error("Error sending conversations to the server:", error);
      setConversations((prev) => [
        ...prev,
        {
          // TODO: Delete
          id: "id",
          type: "server",
          text: "Failed to send conversations to the server",
        },
        {
          id: "id",
          type: "system",
          text: "Failed to send conversations to the server",
        },
      ]);
    }
  }, [conversations]);

  const addClientConversation = useCallback(
    (text: string) => {
      setConversations((prev) => [...prev, { id: "id", type: "client", text }]);
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
