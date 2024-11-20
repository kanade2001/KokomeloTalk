import React from "react";
import { Conversation, MusicConversation } from "../../types/conversation";

interface ConversationListProps {
  conversations: (Conversation | MusicConversation)[];
}

const ConversationList: React.FC<ConversationListProps> = ({ conversations }) => {
  return (
<div className="border border-gray-300 p-2 h-72 overflow-y-scroll mb-2">
  {conversations.map((conversation, index) => (
    <div key={index} className="mb-2">
      <strong>{conversation.type}:</strong> {conversation.text || ""}
    </div>
  ))}
</div>

  );
};

export default ConversationList;
