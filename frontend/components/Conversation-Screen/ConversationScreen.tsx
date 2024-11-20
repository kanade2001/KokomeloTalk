import React from "react";
import { Conversation, MusicConversation } from "../../types/conversation";
import { ClientConversation } from "./components/client-conversation";
import { ServerConversation } from "./components/server-conversation";
import { SystemConversation } from "./components/system-conversation";

interface ConversationListProps {
  conversations: (Conversation | MusicConversation)[];
}

const ConversationList: React.FC<ConversationListProps> = ({
  conversations,
}) => {
  return (
    <div className="border border-gray-300 p-2 h-72 overflow-y-scroll mb-2 ">
      {conversations.map((conversation, index) => (
        <div key={index} className="mb-2">
          {conversation.type === "client" && (
            <ClientConversation text={conversation.text} />
          )}
          {conversation.type === "server" && (
            <ServerConversation text={conversation.text} />
          )}
          {conversation.type === "system" && (
            <SystemConversation text={conversation.text} />
          )}
        </div>
      ))}
    </div>
  );
};

export default ConversationList;
