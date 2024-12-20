export const ClientConversation: React.FC<{ text: string }> = ({ text }) => {
  return (
    <div className="w-full flex justify-end">
      <div
        className="max-w-4xl border-4 border-green-400 rounded-lg p-4 bg-blue-100 text-lg lg:text-xl break-words"
        style={{ wordBreak: "break-word" }}
      >
        {text}
        <div className="absolute right-0 top-full w-0 h-0 border-t-[10px] border-t-black-600 border-l-[100px] border-l-transparent border-r-[10px] border-r-transparent"></div>
      </div>
    </div>
  );
};

