import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./components/login"; // Import Login component

const App = () => (
  <Router>
    <Routes>
      {/* Define the route for the Login page */}
      <Route path="/login" element={<Login />} />

      {/* Example route for a dashboard */}
      <Route path="/dashboard" element={<div>Dashboard Page</div>} />

      {/* Redirect to login page if no other route matches */}
      <Route path="*" element={<Login />} />
    </Routes>
  </Router>
);

export default App;