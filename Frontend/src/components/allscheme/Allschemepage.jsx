"use client"
import React, { useEffect, useState } from "react";
import AllschemeBanner from "./AllschemeBanner";
import SchemeCard from "./SchemeCard";
import { apiHandler } from "../../config/index";
import { API_ENDPOINTS } from "../../config/api";
import { useDispatch } from "react-redux";
import { setScheme } from "@/store/schemeslice";
import { useRouter } from "next/navigation";

const Allschemepage = () => {
  const [users, setUsers] = useState([]);
  const [error, setError] = useState("");
  const dispatch = useDispatch();
  const router = useRouter();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await apiHandler({
          url: API_ENDPOINTS.ALLSCHEME, 
          method: "GET",
        });

        if (response.error) {
          setError(response.message);
        } else {
          setUsers(response.data);
        }
      } catch (err) {
        console.error("Unexpected error:", err);
        setError("Something went wrong");
      }
    };
    fetchData();
  }, []);

  const viewmore = (scheme) => {
    dispatch(setScheme(scheme));
    console.log("scheme", scheme);
    router.push("/schemedetails");
  }

  return (
    <div>
      <AllschemeBanner
        imageUrl={'/e.jpg'}
        height="h-[50vh]"
      />
      <div className="w-full flex justify-center items-center">
        <div className="p-8 text-center containet grid-cols-3 grid gap-5 space-x-3">
          {users.map((s) => (
            <SchemeCard onClick={() => viewmore(s)} key={s.id} scheme={s} />
          ))}
        </div>
      </div>
      {error && <p className="text-red-500">{error}</p>}
    </div>
  );
};

export default Allschemepage;
