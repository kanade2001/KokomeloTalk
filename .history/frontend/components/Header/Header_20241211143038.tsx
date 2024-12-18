import React, { useState } from "react";
import Image from "next/image";

export default function Header() {
    return (
      <header className="flex items-center justify-center border-b ">
        <a>
            <Image src="/cocomelotalk_logo.png"
                    alt="logo"
                    width={250} height={100}
                />
            </a>
      </header>
    )
  }