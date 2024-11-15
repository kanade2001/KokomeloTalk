export interface Conversation {
  id: string;
  type: "client" | "server" | "music";
  text: string;
}

export interface MusicConversation extends Conversation {
  type: "music";
  musicUrl: string;
}
