import React from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const LogoutButton = () => {
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      await axios.get("/api/auth/logout");
      navigate("/login"); // Use React Router for navigation
    } catch (error) {
      console.error("Error during logout:", error);
    }
  };

  return (
    <button
      onClick={handleLogout}
      className="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-700"
    >
      Logout
    </button>
  );
};

export default LogoutButton;
