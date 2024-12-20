// import React from "react";
import { Conversation, MusicConversation } from "../../types/conversation";
import { ClientConversation } from "./components/client-conversation";
import { ServerConversation } from "./components/server-conversation";
import { SystemConversation } from "./components/system-conversation";
import { Music2, AudioWaveformIcon as Waveform } from 'lucide-react';

interface ConversationListProps {
  conversations: (Conversation | MusicConversation)[];
}

const ConversationList: React.FC<ConversationListProps> = ({
  conversations,
}) => {
  return (
    <div className="relative">
      {/* Decorative background elements */}
      <div className="absolute inset-0 bg-gradient-to-br from-purple-500/20 via-pink-500/20 to-blue-500/20 backdrop-blur-xl" />
      <div className="absolute bottom-0 left-0 right-0 h-24 bg-gradient-to-t from-black/10 to-transparent" />
      
      {/* Decorative music elements */}
      <div className="absolute top-4 right-4 text-purple-500/30">
        <Music2 size={24} />
      </div>
      <div className="absolute bottom-4 left-4 text-pink-500/30">
        <Waveform size={24} />
      </div>

      {/* Main conversation container */}
      <div className="relative h-[600px] overflow-y-auto rounded-3xl border border-white/20 bg-white/10 p-4 backdrop-blur-xl">
        <div className="space-y-4">
          {conversations.map((conversation, index) => (
            <div
              key={index}
              className="transition-all duration-300 ease-in-out hover:scale-[1.02]"
            >
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
    </div>
  );
};

export default ConversationList;