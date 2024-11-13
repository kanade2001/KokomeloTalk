export interface Conversation {
  id: string;
  type: "user" | "server" | "music";
}

export interface TextConversation extends Conversation {
  text: string;
}

export interface MusicConversation extends Conversation {
  music: string;
  image: string;
}
