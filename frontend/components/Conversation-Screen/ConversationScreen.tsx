import React, { useEffect, useRef } from "react";
import { Conversation, MusicConversation } from "../../types/conversation";
import { ClientConversation } from "./components/client-conversation";
import { ServerConversation } from "./components/server-conversation";
import { SystemConversation } from "./components/system-conversation";
import { MusicConversationComponent } from "./components/music-conversation";
interface ConversationListProps {
  conversations: (Conversation | MusicConversation)[];
}

const ConversationList: React.FC<ConversationListProps> = ({
  conversations,
}) => {
  // スクロール対象のコンテナを参照する
  const containerRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    // conversationsが更新されるたびにスクロール位置を最下部に
    if (containerRef.current) {
      containerRef.current.scrollTop = containerRef.current.scrollHeight;
    }
  }, [conversations]);

  return (
    <div
      ref={containerRef}
      className="border border-gray-300 p-2 h-[600px] overflow-y-scroll mb-2 bg-gradient-to-br from-green-300 to-green-100"
    >
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
          {conversation.type === "music" && (
            <MusicConversationComponent
              text={conversation.text}
              artist={(conversation as MusicConversation).music_artist}
              url={(conversation as MusicConversation).music_url}
            />
          )}
        </div>
      ))}
    </div>
  );
};

export default ConversationList;
