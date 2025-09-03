import { FaStar } from "react-icons/fa";
import { HiOutlineExternalLink } from "react-icons/hi";

export default function Citycard({ name, priceRange, rating, reviews, img, properties }) {
  return (
    <div className="w-[280px] h-[320px]  border-t-5 border-1  border-t-[#ffa2b6] border-gray-300 rounded-lg p-4 flex flex-col justify-between bg-white">

      {/* Top section */}
      <div>
        {/* Title and link */}
        <div className="flex justify-between items-center mb-2">
          <h3 className="text-lg font-semibold text-gray-800">{name}</h3>
          <HiOutlineExternalLink className="text-gray-500" size={16} />
        </div>

        {/* Price range */}
        <p className="text-sm text-gray-600 mb-3">{priceRange}</p>

        {/* Rating and reviews */}
        <div className="flex items-center justify-start gap-4 mb-4">
          <div className="flex items-center text-gray-800 font-medium">
            <span>{rating}</span>
            <FaStar className="text-yellow-500 ml-1" size={14} />
          </div>
          <span className="text-sm text-gray-500">{reviews} Reviews</span>
        </div>
      </div>

      {/* Bottom section */}
      <div className="relative  bg-[#ffeff4] rounded-md px-3 h-16 flex items-end pb-2 text-center font-semibold text-red-600 cursor-pointer hover:bg-blue-100 transition-colors duration-200">
        {properties}→
        <div className="absolute -top-10 left-3 w-16 h-16 overflow-hidden rounded-full mx-auto border border-gray-300">
          <img
            src={img}
            alt={name}
            className="w-full h-full object-cover"
            onError={(e) => {
              e.target.src = "https://via.placeholder.com/64x64?text=City";
            }}
          />
        </div>
      </div>
    </div>
  );
}
