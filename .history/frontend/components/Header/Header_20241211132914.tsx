import React, { useState } from "react";

export default function Header() {
    return (
      <header className="flex items-center justify-between p-4 border-b">
        <div className="flex items-center space-x-4">
          <div>
            <h1 className="text-xl font-semibold justify-center">COCOMELO TALK</h1>
          </div>
        </div>
      </header>
    )
  }