// MainLayout.jsx
"use client";
import React, { useState } from "react";
import Sidebar from "./Sidebar";
import Dashboard from "./Dashboard";
import { useSelector } from "react-redux";
import Summary from "./Summary";

const headings = ["Dashboard", "Reservation", "Summary"];

const MainLayout = () => {
  const [selected, setSelected] = useState("Dashboard");
   const data = useSelector((state) => state.scheme.scheme);

   const arrayData = Array.isArray(data) ? data : data ? [data] : [];

  const renderContent = () => {
    switch (selected) {
      case "Dashboard":
        return <Dashboard data={arrayData} />;
      case "Summary":
        return <Summary data={data} />;
    }
  };

  return (
    <div className="flex">
      <Sidebar headings={headings} selected={selected} setSelected={setSelected} />
      <div className="flex-1">{renderContent()}</div>
    </div>
  );
};

export default MainLayout;
