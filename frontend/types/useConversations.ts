import { useCallback, useState } from "react";
import { v4 as uuidv4 } from "uuid";
import { Conversation, MusicConversation } from "./conversation";

const API_URL = "http://localhost:8000";

export const useConversations = () => {
  const [conversations, setConversations] = useState<
    (Conversation | MusicConversation)[]
  >([
    { type: "server", id: uuidv4(), text: "こんにちは！COCOMELO TALKです！" },
    {
      type: "server",
      id: uuidv4(),
      text: "文章から感情を推定しておすすめの音楽を教えるよ",
    },
    {
      type: "server",
      id: uuidv4(),
      text: "下のメッセージ欄から何か話しかけてみてね！",
    },
  ]);

  const getServerConversation = useCallback(
    async (text: string) => {
      try {
        console.log(text);
        const response = await fetch(`${API_URL}/conversation/`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          // body: JSON.stringify(conversations), // 会話リストを送信
          body: JSON.stringify({ text }),
        });

        if (!response.ok) {
          // サーバーからのレスポンスがエラーだった場合
          throw new Error("Failed to send conversations to the server");
        }

        const data: (Conversation | MusicConversation)[] =
          await response.json();
        console.log("Server response:", data);
        setConversations((prev) => [
          ...prev,
          ...data.map((item) => ({ ...item, id: uuidv4() })),
        ]);
      } catch (error) {
        // サーバーへのリクエストが失敗した場合
        console.error("Error sending conversations to the server:", error);
        setConversations((prev) => [
          ...prev,
          {
            id: uuidv4(),
            type: "system",
            text: "Failed to send conversations to the server",
          },
        ]);
      }
    },
    [conversations]
  );

  const addClientConversation = useCallback(
    (text: string) => {
      setConversations((prev) => [
        ...prev,
        { id: uuidv4(), type: "client", text },
      ]);
      getServerConversation(text);
    },
    [getServerConversation]
  );

  return {
    conversations,
    addClientConversation,
    getServerConversation,
  };
};
