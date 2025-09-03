import React from "react";

const PropertyCard = ({ imageUrl, title, description, location, priceRange }) => {
  return (
    <div className="max-w-xs bg-white shadow-md rounded-xl overflow-hidden border border-gray-200">
      {/* Image */}
      <img
        src={imageUrl}
        alt={title}
        className="w-full h-44 object-cover"
      />

      {/* Content */}
      <div className="p-4">
        <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
        <p className="text-sm text-gray-600 mt-1">{description}</p>
        <p className="text-sm text-gray-500">{location}</p>

        {/* Price */}
        <p className="text-lg font-semibold text-gray-900 mt-2">{priceRange}</p>

        {/* Button */}
        <button className="mt-3 w-full border border-purple-500 text-purple-500 rounded-lg py-2 text-sm font-medium hover:bg-purple-50 transition duration-300">
          Contact
        </button>
      </div>
    </div>
  );
};

export default PropertyCard;
