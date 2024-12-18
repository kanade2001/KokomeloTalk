import React, { useState } from "react";
import Image from "next/image";

export default function Header() {
    return (
      <header className="flex items-center justify-center p-4 border-b ">
        <a>
            <Image src="../public/cocomelotalk_logo.png"
                    alt="logo"
                    className="h-10 w-10 object-cover"
                />
            </a>
      </header>
    )
  }