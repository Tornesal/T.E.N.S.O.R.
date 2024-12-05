import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./components/login";
import Register from "./components/register";
import Dashboard from "./components/dashboard"; // Import Dashboard component

const App = () => (
  <Router>
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/dashboard" element={<Dashboard />} />

        {/* Redirect to login page if the route is not found */}
      <Route path="*" element={<Login />} />
    </Routes>
  </Router>
);

export default App;