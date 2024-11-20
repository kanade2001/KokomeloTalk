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
    onSend(input); // 親コンポーネントに入力内容を渡す
    setInput(""); // 入力フィールドをリセット
  };

  return (
      <div className="flex gap-2">
        <input
          type="text"
          value={input}
          onChange={handleInputChange}
          placeholder="Type your message..."
          className="flex-1 p-2 text-base border border-gray-300 rounded"
        />
        <button
          onClick={handleSend}
          className="px-4 py-2 text-base font-medium text-white bg-blue-500 rounded hover:bg-blue-600 focus:outline-none"
        >
          Send
        </button>
      </div>
  );
};

export default UserInput;
