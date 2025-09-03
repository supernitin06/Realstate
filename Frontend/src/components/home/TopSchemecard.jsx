'use client'


export default function PropertyCard({ img, title, marketer, details, location, priceRange }) {
    return (
        <div className="relative w-full h-[340px] group cursor-pointer rounded-xl overflow-hidden shadow-lg">
            {/* Background Image */}
            <img
                src={img}
                alt={title}
                className="absolute inset-0 w-full h-full object-cover"
                onError={(e) => {
                    e.target.src = "/villa.jpg";
                }}
            />

            {/* Dark Gradient Overlay */}

            {/* Text Content */}
            <div className="absolute bottom-0 p-4 w-full text-white">
                {/* Title & Price */}
                <div className="flex justify-between items-center">
                    <div>
                        <h3 className="text-lg font-semibold">{title}</h3>
                        <p className="text-sm text-gray-300">Mktd. by {marketer}</p>
                    </div>
                    <span className="text-lg font-bold">{priceRange}</span>
                </div>

                {/* Details & Location */}
                <p className="text-sm mt-2">{details}</p>
                <p className="text-xs text-gray-300">{location}</p>
            </div>

            <div
                className="
                      absolute group-hover:h-[100%] duration-600 cursor-pointer  w-full h-0 bg-gradient-to-t from-black/30 via-black/20 to-transparent          
                    "
            ></div>
        </div>
    );
}
