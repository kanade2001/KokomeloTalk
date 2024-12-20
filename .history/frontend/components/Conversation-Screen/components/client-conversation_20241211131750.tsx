export const ClientConversation: React.FC<{ text: string }> = ({ text }) => {
  return (
    <div className="w-full flex justify-end">
      <div
        className="max-w-4xl border-2 border-blue-600 rounded-lg p-2 bg-blue-100 break-words"
        style={{ wordBreak: "break-word" }}
      >
        {text}
      </div>
    </div>
  );
};
