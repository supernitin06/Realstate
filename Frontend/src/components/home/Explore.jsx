import React from 'react'

const button = ["Affordable Housing", "Luxury Homes", "Commercial Properties", "Plots and Land", "Rental Properties"]

const Explore = () => {
  return (
    <div className='w-full flex justify-center mb-10 mt-28 items-center '>
      <div className='container flex flex-col gap-10 justify-center items-center '>
        <div className='w-full text-5xl font-semibold  flex items-center justify-start'>
          Explore Top Picks
        </div>
        <div className='grid grid-cols-1 border-b-2  border-0 sm:grid-cols-2 md:grid-cols-5 lg:grid-cols-5 gap-6 w-full'>
              {button.map((item, index) => (
          <div key={index} className='w-full h-20 hover:bg-gray-400 hover:scale-105  bg-gray-200 flex items-center justify-center  shadow-md hover:shadow-lg transition-shadow duration-500 cursor-pointer'>
            <span className='text-2xl  font-light text-gray-900'>{item}</span>
          </div>
              ))}
        </div>
      </div>

    </div>
  )
}

export default Explore