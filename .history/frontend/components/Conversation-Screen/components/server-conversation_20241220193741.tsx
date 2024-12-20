export const ServerConversation: React.FC<{ text: string }> = ({ text }) => {
  return (
    <div className="w-full flex justify-start">
      <div
        className="max-w-4xl border-4 border-white-800 rounded-3xl p-4 bg-blue-100 text-lg lg:text-xl break-words rounded-tl-none"
        style={{ wordBreak: "break-word" }}
      >
        {text}
      </div>
    </div>
  );
};
