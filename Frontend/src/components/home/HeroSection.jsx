import Image from 'next/image'
import React from 'react'
import { FaMapMarkerAlt, FaHome, FaSearch } from "react-icons/fa";
import { MdCurrencyRupee } from "react-icons/md";


const HeroSection = () => {
    return (
      <div className="relative w-full h-[600px]">
        <Image
          src="/vecteezy_attractive-and-modern-house_24685666.jpg"
          alt="Hero Image"
          fill
          className="object-fit"
        />

        <div className="absolute top-0 left-0 w-full gap-6 h-full bg-black/50 flex flex-col justify-center items-center">
             <div className="text-white text-5xl font-light tracking-wide">
        Start your <span className="font-semibold">#ApnaGharApnaKal</span> Journey
      </div>

      {/* Search Bar */}
      <div className="flex items-center justify-between px-2 bg-white shadow-lg rounded-full overflow-hidden border border-gray-200 w-[720px] mx-auto transition-all duration-300 hover:shadow-xl">
        {/* Location */}
        <div className="flex items-center px-6 py-5 border-r border-gray-300 hover:bg-gray-50 transition-colors duration-200">
          <FaMapMarkerAlt className="text-[#e43d12] mr-2 text-lg" />
          <span className="bg-[#e43d12]/10 text-[#e43d12] px-3 py-1 rounded-md text-base font-medium">
            Noida
          </span>
          <span className="ml-3 text-gray-500 text-base hover:text-[#e43d12] cursor-pointer">
            Add more...
          </span>
        </div>

        {/* Property Type */}
        <div className="flex items-center px-5 py-5 border-r border-gray-300 hover:bg-gray-50 transition-colors duration-200">
          <FaHome className="text-[#e43d12] mr-2 text-lg" />
          <span className="text-gray-700 text-base font-medium">Flat +1</span>
          <span className="ml-2 text-gray-400">▼</span>
        </div>

        {/* Budget */}
        <div className="flex items-center px-5 py-5 border-r border-gray-300 hover:bg-gray-50 transition-colors duration-200">
          <MdCurrencyRupee className="text-[#e43d12] mr-2 text-lg" />
          <span className="text-gray-700 text-base font-medium">Budget</span>
          <span className="ml-2 text-gray-400">▼</span>
        </div>

        {/* Search Button */}
        <button className="flex items-center ml-2 bg-[#e43d12] hover:bg-[#c6350f] transition-colors duration-200 text-white font-semibold px-6 py-4 rounded-full">
          <FaSearch className="mr-2" /> Search
        </button>
      </div>
        </div>
      </div>
    );
}

export default HeroSection
