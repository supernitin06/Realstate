// Summary.jsx
"use client";
import React from "react";

const Summary = ({ data }) => {
  if (!data) return <p>No data available</p>;
 console.log(data)
  const filename = data.filename || "No filename";
  const summaryContent =
    data.summaries && data.summaries.length >= 0
      ? data.summaries[0].content
      : "No summary available";

  return (
    <div className="border rounded-lg p-4 shadow hover:shadow-lg transition mb-4">
      {/* Dark heading */}
      <h2 className="text-xl font-bold text-gray-900 mb-2">{filename}</h2>

      {/* Normal text content */}
      <p className="text-gray-700 mb-2">{summaryContent}</p>

      {/* Optional label showing summary count */}
      {data.summaries && data.summaries.length > 0 && (
        <span className="text-sm text-gray-500">
          Summary {data.summaries.length}
        </span>
      )}
    </div>
  );
};

export default Summary;
