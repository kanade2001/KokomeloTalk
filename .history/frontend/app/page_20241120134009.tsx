"use client";
import React from "react";
import { useConversations } from "../types/useConversations";
import ConversationScreen from "../components/Conversation-Screen/ConversationScreen";
import UserInput from "../components/User-Input/UserInput";

const App = () => {
  const { conversations, addClientConversation, getServerConversation } =
    useConversations();

  const handleSend = async (input: string) => {
    if (input.trim() === "") return; // 入力が空の場合は何もしない
    addClientConversation(input); // 会話リストに追加
  };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
      <h1>COCOMELO TALK</h1>
      <ConversationScreen conversations={conversations} />
      <UserInput onSend={handleSend} />
    </div>
  );
};

export default App;
