import React, { useState } from "react";

export default function Header() {
    return (
      <header className="flex items-center justify-between p-4 border-b">
        <div className="flex items-center space-x-4">
          <div>
            <h1 className="text-xl font-semibold">COCOMELO TALK</h1>
            <p className="text-sm text-green-500 flex items-center">
              <span className="w-2 h-2 bg-green-500 rounded-full mr-2"></span>
              Online
            </p>
          </div>
        </div>
      </header>
    )
  }