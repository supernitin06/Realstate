import React from 'react'
import TopSchemecard from "./TopSchemecard";

const TopSchemes = () => {
    return (
        <div className='w-full flex justify-center mb-10 mt-10 items-center '>
            <div className='container flex flex-col gap-10 justify-center items-center '>
                <div className='w-full text-5xl font-semibold  flex items-center justify-start'>
                    Top Rated Schemes
                </div>
                <div className='grid grid-cols-1 sm:grid-cols-2 md:grid-cols-2 lg:grid-cols-2 gap-6 w-full'>
                    <TopSchemecard
                        img="/villa.jpg"
                        title="Radhaya Urbanity"
                        marketer="Ramji Corp"
                        details="3, 4 BHK Apartments"
                        location="Aya Nagar, South Delhi, New Delhi"
                        priceRange="₹1.38 Cr - 2.13 Cr"
                    />
                    <TopSchemecard
                        img="/ss.webp"
                        title="Radhaya Urbanity"
                        marketer="Ramji Corp"
                        details="3, 4 BHK Apartments"
                        location="Aya Nagar, South Delhi, New Delhi"
                        priceRange="₹1.38 Cr - 2.13 Cr"
                    />
                </div>
            </div>
        </div>
    )
}

export default TopSchemes