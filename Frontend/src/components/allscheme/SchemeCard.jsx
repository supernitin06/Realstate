"use client"
import React from "react";

function SchemeCard({ scheme, onViewMore , onClick}) {
  const handleViewMore = () => {
    if (onViewMore) onViewMore(scheme);
  };

  const API_URL = "http://127.0.0.1:8000"; // FastAPI server
  console.log(scheme)

  return (
    <article
      onClick={onClick} // <-- attach onClick here
      className="max-w-sm bg-white rounded-2xl shadow-lg overflow-hidden transform hover:-translate-y-1 transition-transform duration-200"
      aria-labelledby={`scheme-${scheme.id}-title`}
    >
      <div className="h-44 w-full bg-gray-100 flex items-center justify-center overflow-hidden">
        {scheme.images && scheme.images.length > 0 ? (
          <img
            src={`${API_URL}/uploads/images/${scheme.images[0].filename}`}
            alt={`${scheme.filename} image`}
            className="w-full h-full object-cover"
            loading="lazy"
          />


        ) : (
          <div className="text-gray-400 text-sm">No image available</div>
        )}
      </div>

      <div className="p-4">
        <h3
          id={`scheme-${scheme.id}-title`}
          className="text-lg font-semibold text-slate-900 truncate"
          title={scheme.filename}
        >
          {scheme.filename}
        </h3>

        {scheme.location && (
          <p className="text-sm text-slate-500 mt-1">{scheme.location}</p>
        )}

        {scheme.summary && (
          <p className="mt-3 text-sm text-slate-600 line-clamp-3">
            {scheme.summaries.summary}
          </p>
        )}

        <div className="mt-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <button
              onClick={handleViewMore}
              className="inline-flex items-center gap-2 px-3 py-1.5 rounded-md text-sm font-medium bg-indigo-600 text-white hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-300"
            >
              View more
            </button>

            <a
              href="#"
              onClick={(e) => e.preventDefault()}
              className="text-sm text-slate-500 hover:text-slate-700"
            >
              Save
            </a>
          </div>

          <span className="text-xs text-slate-400">ID: {scheme.id}</span>
        </div>
      </div>
    </article>
  );
}
export default SchemeCard;