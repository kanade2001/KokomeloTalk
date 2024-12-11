import React, { useState } from "react";

export default function Header() {
    return (
      <header className="flex items-center justify-center p-4 border-b ">
            <img src="../public/cocomelotalk_logo"
                 alt="logo"
                 className="h-10 w-10 object-cover"
            />
      </header>
    )
  }