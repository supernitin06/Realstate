import React from "react";
import PropTypes from "prop-types";

export default function AllschemeBanner({ imageUrl, height = "h-96" }) {
  return (
    <div
      className={`relative w-full  overflow-hidden ${height}`}
      aria-label="Image banner"
    >
      <img
        src={imageUrl}
        alt="Banner"
        className="w-full h-full object-fit"
      />

      <div className="absolute inset-0 bg-black/30  ">

      </div>
    </div>
  );
}

AllschemeBanner.propTypes = {
  imageUrl: PropTypes.string.isRequired,
  height: PropTypes.string,
};
