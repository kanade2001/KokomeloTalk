export const SystemConversation: React.FC<{ text: string }> = ({ text }) => {
  return (
    <div className="w-full border border-2 border-red-600 rounded-lg p-2 text-center text-red-600">
      {text}
    </div>
  );
};
