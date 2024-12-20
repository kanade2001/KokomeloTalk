export const ServerConversation: React.FC<{ text: string }> = ({ text }) => {
  return (
    <div className="w-full flex justify-start">
      <div
        className="max-w-4xl border-4 border-white-800 rounded-lg p-4 bg-white-100 text-lg lg:text-xl break-words"
        style={{ wordBreak: "break-word" }}
      >
        {text}
      </div>
    </div>
  );
};
