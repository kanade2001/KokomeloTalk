export const ServerConversation: React.FC<{ text: string }> = ({ text }) => {
  return (
    <div className="w-full flex justify-start">
      <div
        className="max-w-4xl border border-2 border-white rounded-lg border-gray-600 bg-gray-100 p-2 break-words"
        style={{ wordBreak: "break-word" }}
      >
        {text}
      </div>
    </div>
  );
};
