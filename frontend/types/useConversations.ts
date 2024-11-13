import { useCallback, useState } from "react";
import { MusicConversation, TextConversation } from "./conversation";

export const useConversations = () => {
  const [conversations, setConversations] = useState<
    (TextConversation | MusicConversation)[]
  >([]);

  const addUserConversation = useCallback((text: string) => {
    setConversations((prev) => [...prev, { id: "id", type: "user", text }]);
  }, []);

  const sendConversationsToServer = useCallback(async () => {
    try {
      const response = await fetch(
        "https://your-server-endpoint.com/api/conversations",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(conversations),
        }
      );

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
          id: "id",
          type: "server",
          text: "Failed to send conversations to the server",
        },
      ]);
    }
  }, [conversations]);

  return {
    conversations,
    addUserConversation,
    sendConversationsToServer,
  };
};
