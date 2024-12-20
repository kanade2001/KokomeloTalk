import React from "react";
import { Conversation, MusicConversation } from "../../types/conversation";
import { ClientConversation } from "./components/client-conversation";
import { ServerConversation } from "./components/server-conversation";
import { SystemConversation } from "./components/system-conversation";
import Image from "next/image";

interface ConversationListProps {
  conversations: (Conversation | MusicConversation)[];
}

const ConversationList: React.FC<ConversationListProps> = ({
  conversations,
}) => {
  return (
    <div className="border border-gray-300 p-2 h-[600px] overflow-y-scroll mb-2 bg-pink-200">
      <a>
        <Image 
          src="/talk_bg.png"
          alt="logo"
          width={500}
          height={10}
        />
      </a>
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
