import { FaLandmark } from "react-icons/fa";
import { IoDocumentTextOutline } from "react-icons/io5";

export default function FeatureCards() {
  const cards = [
    {
      title: "Find Best Govt Yojna !!",
      button: "Explore Now",
      color: "bg-[#d6536d]", // Deep blue
      icon: <FaLandmark  size={80} className="text-gray-200" />,
    },
    {
      title: "Top Scheme in India",
      button: "Explore Now",
      color: "bg-[#efb11d]", // Magenta-ish
      icon: <IoDocumentTextOutline size={80} className="text-gray-200" />,
    },
    {
      title: "Explore India's Top Residential Cities List",
      button: "Explore Now",
      color: "bg-[#ffa2b6]", // Yellow
      icon: <IoDocumentTextOutline size={80} className="text-gray-200" />,
    },
    {
      title: "Helping you to find your dream Property",
      button: "Explore Now",
      color: "bg-[#afd275]", // Teal
      icon: <IoDocumentTextOutline size={80} className="text-gray-200" />,
    },
  ];

  return (
    <div className="w-full bg-[#ebe9e1] py-10 flex justify-center items-center">
      <div className="flex flex-wrap gap-6 justify-center py-8">
        {cards.map((card, i) => (
          <div
            key={i}
            className={`${card.color} ${card.textColor || "text-white"
              } relative rounded-lg p-6 w-88 flex flex-col justify-between shadow-md hover:shadow-2xl transition-all duration-300 cursor-pointer`}
          >
            {/* Icon in top-right */}
            <div className="absolute bottom-3  right-4 opacity-40">{card.icon}</div>

            {/* Title */}
            <p
              className={`text-2xl leading-snug ${card.textColor ? card.textColor : "text-white"
                }`}
            >
              {card.title}
            </p>

            {/* Button */}
            <button className="mt-6 w-[160px] inline-flex items-center hover:translate-x-1 duration-300 bg-white text-black px-4 py-3 rounded-xl font-medium shadow hover:shadow-xl transition">
              {card.button} <span className="ml-2">→</span>
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
