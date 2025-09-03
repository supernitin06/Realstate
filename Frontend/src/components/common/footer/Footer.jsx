import {
  Facebook,
  Instagram,
  Twitter,
  Github,
  Youtube,
} from "lucide-react";

const Footer = () => {
  return (
    <footer className="bg-[#244855] text-white flex flex-col justify-between px-4 pt-16 pb-8 ">
      <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-4 gap-12">
        {/* Left section */}
        <div>
          <h1 className="text-2xl font-bold flex items-center gap-2">
            {/* <img
              src=""
              className="h-10 w-56"
              alt="Flowbite Logo"
            /> */}
          </h1>
          <p className="mt-4 text-md font-extralight max-w-sm">
            Trusted in more than 100 countries & 5 million customers. Follow us on social media.
          </p>

          <div className="flex mt-4 gap-5 text-white">
            <Facebook size={24} className="hover:text-gray-300 cursor-pointer" />
            <Instagram size={24} className="hover:text-gray-300 cursor-pointer" />
            <Twitter size={24} className="hover:text-gray-300 cursor-pointer" />
            <Github size={24} className="hover:text-gray-300 cursor-pointer" />
            <Youtube size={24} className="hover:text-gray-300 cursor-pointer" />
          </div>
        </div>

        
        {/* Quick Links */}
        <div className="md:pl-10 pl-2">
          <h3 className="font-semibold text-xl mb-3">Quick Links</h3>
          <ul className="space-y-2 text-md font-extralight">
            <li><a href="/" className="hover:underline">HOME</a></li>
            <li><a href="/about" className="hover:underline">ABOUT</a></li>
            <li><a href="/events/events" className="hover:underline">EVENTS</a></li>
            <li><a href="/contact" className="hover:underline">CONTACT</a></li>
          </ul>
        </div>


        {/* Contact section */}
        <div>
          <h3 className="font-semibold text-xl mb-3">Get In Touch</h3>
          <p className="text-md font-extralight mb-1">support@pagedone.com</p>
          <p className="text-md font-extralight mb-1">+91 945 658 3256</p>
          <p className="text-md font-extralight">61-A, Elm street, Gujarat, India.</p>
        </div>

 

        {/* Newsletter */}
        <div>
          <h3 className="font-semibold text-xl mb-3">Newsletter</h3>
          <div className="flex flex-col space-y-3 text-white">
            <input
              type="email"
              placeholder="Your email here..."
              className="p-3 rounded-full border border-gray-300 focus:outline-none text-white font-bold"
            />
            <button className="bg-[#964734] hover:bg-black text-white py-2 rounded-full transition">
              Subscribe
            </button>
          </div>
        </div>
      </div>

      {/* Bottom bar */}
      <div className="border-t border-gray-600 mt-12 pt-6 text-sm flex flex-col md:flex-row justify-between items-center text-gray-400">
        <p>©pagedone 2023, All rights reserved.</p>
        <div className="flex space-x-6 mt-4 md:mt-0">
          <a href="#" className="hover:underline">Terms</a>
          <a href="#" className="hover:underline">Privacy</a>
          <a href="#" className="hover:underline">Cookies</a>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
