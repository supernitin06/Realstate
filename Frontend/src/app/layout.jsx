
"use client"
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import Navbar from "@/components/common/navbar/Navbar";
import Footer from "@/components/common/footer/Footer";
import { Provider } from "react-redux";
import store, { persistor } from "../store/schemestore";
import { PersistGate } from "redux-persist/integration/react";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body
        suppressHydrationWarning={true}
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <div className="sticky top-0 z-50">
          <Navbar />
        </div>

        {/* Add padding so content starts below navbar */}
        <main className="">
          <Provider store={store}>
            <PersistGate loading={null} persistor={persistor}>

              {children}
            </PersistGate>
          </Provider >
        </main>
        <div>
          <Footer />
        </div>
      </body>
    </html>
  );
}
