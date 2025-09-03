import React from 'react'
import HeroSection from '../../../components/home/HeroSection'
import FeatureCards from '../../../components/home/FeatureCards'
import CitySwiper from '../../../components/home/CitySwiper'
import TopSchemes from '../../../components/home/TopSchemes'
import Explore from "../../../components/home/Explore";

const Homepage = () => {
  return (
    <div>
<HeroSection />
<FeatureCards />
<CitySwiper/>
<TopSchemes/>
<Explore/>
    </div>
  )
}

export default Homepage