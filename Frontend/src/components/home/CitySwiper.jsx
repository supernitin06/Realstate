"use client";
import { Swiper, SwiperSlide } from "swiper/react";
import "swiper/css";
import "swiper/css/navigation";
import "swiper/css/autoplay";
import Citycard from "./Citycard";
import { Navigation, Autoplay } from "swiper/modules";
import { GrNext, GrPrevious } from "react-icons/gr";

export default function CitySwiper() {
  const localities = [
    {
      name: "Delhi (DDA Housing Scheme)",
      priceRange: "Subsidised rates (varies by plot/flat size)",
      rating: 4.0,
      reviews: 120,
      img: "/01.jpg",
      properties: "213 Schems (2023)",
    },
    {
      name: "Urban PMAY-U (All India)",
      priceRange: "6.5%–3% interest subsidy on loans",
      rating: 4.2,
      reviews: 450,
      img: "/01.jpg",
      properties: "400+ Schemes",
    },
    {
      name: "Rural PMAY-G (Rural India)",
      priceRange: "₹1.2L–₹1.3L grant (region-dependent)",
      rating: 4.1,
      reviews: 380,
      img: "/01.jpg",
      properties: "213 Scheems (2023)",
    },
    {
      name: "Odisha Affordable Housing Projects",
      priceRange: "EWS flats, moderate pricing",
      rating: 4.3,
      reviews: 85,
      img: "/01.jpg",
      properties: "400 schemes",
    },
    {
      name: "Lucknow Township Scheme (UP)",
      priceRange: "State-subsidised greenfield townships",
      rating: 4.0,
      reviews: 60,
      img: "/01.jpg",
      properties: "200 schemes",
    },

  ];


  return (
    <div className="container mx-auto px-4 py-10">
      <div className="flex flex-col lg:flex-row gap-8 items-center">
        {/* Left side content */}
        <div className="w-full lg:w-[290px] h-[320px] bg-[#ffa2b6] flex flex-col justify-center items-center p-6 rounded-lg">
          <h2 className="text-4xl  text-gray-800 mb-4">Popular Scheems</h2>
          <p className="text-gray-700 text-center">
            Discover the most sought-after areas with great property options
          </p>
        </div>

        {/* Swiper container */}
        <div className="relative w-full lg:w-[80%]  px-8 h-[400px]">
          <Swiper
            className="h-full"
            modules={[Navigation, Autoplay]}
            navigation={{
              nextEl: ".next-btn",
              prevEl: ".prev-btn",
            }}
            loop={true}
            autoplay={{
              delay: 3000,
              disableOnInteraction: false,
            }}
            grabCursor={true}
            spaceBetween={20}
            slidesPerView={1}
            breakpoints={{
              640: { slidesPerView: 2 },
              768: { slidesPerView: 3 },
              1024: { slidesPerView: 4 },
            }}
          >
            {localities.map((loc, i) => (
              <SwiperSlide key={i} className="h-auto">
                <div className="h-full flex items-center">
                  <Citycard {...loc} />
                </div>
              </SwiperSlide>
            ))}
          </Swiper>

          {/* Navigation buttons */}
          <button className="absolute hidden md:flex -left-5 top-1/2 -translate-y-1/2 prev-btn text-black  p-3 rounded-full z-10 hover:bg-[#ffa2b6] cursor-pointer  transition-colors duration-300 shadow-lg">
            <GrPrevious size={20} />
          </button>
          <button className="absolute hidden md:flex -right-5 top-1/2 -translate-y-1/2 next-btn text-black  p-3 rounded-full z-10 hover:bg-[#ffa2b6] cursor-pointer  transition-colors duration-300 shadow-lg">
            <GrNext size={20} />
          </button>
        </div>
      </div>
    </div>
  );
}
