import React, { useState } from "react";

interface InputBoxProps {
  onSend: (input: string) => void;
}

const UserInput: React.FC<InputBoxProps> = ({ onSend }) => {
  const [input, setInput] = useState("");

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInput(e.target.value);
  };

  const handleSend = () => {
    if (input.trim() !== "") {
      onSend(input); // 親コンポーネントに入力内容を渡す
      setInput(""); // 入力フィールドをリセット
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (!e.nativeEvent.isComposing && e.key === "Enter") {
      // 日本語入力の確定中ではない場合に送信
      handleSend();
    }
  };

  return (
    <div className="flex gap-2">
      <input
        type="text"
        value={input} 
        onChange={handleInputChange}
        onKeyDown={handleKeyDown} // Enterキー対応
        placeholder="Type your message..."
        className="flex-1 p-2 text-base border-gray-300 rounded border focus:outline-none focus:ring-green-300 focus:border-green-300"
      />
      <button
        onClick={handleSend}
        className="px-4 py-2 text-base font-medium text-white bg-green-500 rounded hover:bg-green-600 focus:outline-none"
      >
        Send
      </button>
    </div>
  );
};

export default UserInput;
