import React, { useState } from "react";
import Image from "next/image";

export default function Header() {
    return (
      <header className="flex items-center justify-center p-4 border-b ">
        <a>
            <Image src="/cocomelotalk_logo.png"
                    alt="logo"
                    width={55} height={60}
                />
            </a>
      </header>
    )
  }