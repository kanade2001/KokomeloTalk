export interface Conversation {
  id: string;
  type: "client" | "server" | "system" | "music";
  text: string;
}

export interface MusicConversation extends Conversation {
  type: "music";
  musicUrl: string;
}
