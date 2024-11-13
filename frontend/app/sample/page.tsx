"use client";
import { useState } from "react";

import { useConversations } from "@/types/useConversations";

export default function Sample() {
  const { conversations, addClientConversation } = useConversations();
  const [clientInput, setClientInput] = useState("");
  return (
    <div>
      <h1>Sample</h1>

      <ul>
        {conversations.map(
          (
            conversation // Conversationsをループで取り出す
          ) => (
            <li key={conversation.id}>
              {(() => {
                switch (
                  conversation.type // typeによって表示形式を変更
                ) {
                  case "client":
                    return (
                      <>
                        <strong>Client:</strong>
                        <p>{conversation.text}</p>
                      </>
                    );
                  case "server":
                    return (
                      <>
                        <strong>Server:</strong>
                        <p>{conversation.text}</p>
                      </>
                    );
                  case "music":
                    return (
                      <>
                        <strong>Music:</strong>
                        <p>{conversation.text}</p>
                      </>
                    );
                  default:
                    return null;
                }
              })()}
            </li>
          )
        )}
      </ul>
      <input
        type="text"
        value={clientInput}
        onChange={(e) => setClientInput(e.target.value)}
      />
      <button
        onClick={() => {
          addClientConversation(clientInput);
          setClientInput("");
        }}
      >
        Send
      </button>
    </div>
  );
}
