import Image from "next/image";

export default function Header() {
  return (
    <header className="flex items-center border-b ">
      <a>
        <Image
          src="/cocomelotalk_logo.png"
          alt="logo"
          width={400}
          height={7}
        />
      </a>
    </header>
  );
}
