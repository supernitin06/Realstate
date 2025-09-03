// Sidebar.jsx
"use client";
import React from "react";

const Sidebar = ({ headings, selected, setSelected }) => {
  return (
    <div className="w-1/4 h-screen bg-gray-100 p-4">
      <ul className="space-y-4">
        {headings.map((heading) => (
          <li
            key={heading}
            className={`cursor-pointer p-2 rounded ${
              selected === heading ? "bg-blue-500 text-white" : "hover:bg-gray-200"
            }`}
            onClick={() => setSelected(heading)}
          >
            {heading}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Sidebar;
