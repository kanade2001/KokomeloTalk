export const MusicConversationComponent: React.FC<{
  text: string;
  artist: string;
  url: string;
}> = ({ text, artist, url }) => {
  return (
    <div className="w-full flex justify-center">
      <a
        className="w-full grid grid-cols-[auto_1fr] gap-x-4 border-4 border-green-800 rounded-3xl p-4 bg-blue-100 text-lg lg:text-xl break-words no-underline hover:bg-blue-300 cursor-pointer"
        href={url}
        target="_blank"
        rel="noopener noreferrer"
      >
        <p className="font-bold">曲名:</p>
        <p>{text}</p>
        <p className="font-bold">アーティスト:</p>
        <p>{artist}</p>
      </a>
    </div>
  );
};
