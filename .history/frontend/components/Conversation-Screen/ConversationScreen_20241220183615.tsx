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
    <div 
    className="relative h-[600px] overflow-y-auto rounded-3xl border border-white/20 bg-white/10 backdrop-blur-xl p-6 space-y-4"
    style={{
      scrollbarWidth: 'thin',
      scrollbarColor: 'rgba(255, 255, 255, 0.3) transparent'
    }}
  >
    <div className="border border-gray-300 p-2 h-[600px] overflow-y-scroll mb-2 bg-pink-200">
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
    </div>
  );
};

export default ConversationList;
