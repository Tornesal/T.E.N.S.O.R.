import React, { useState, useEffect } from "react";
import axios from "axios";
import CalendarHeatmap from "react-calendar-heatmap";
import "react-calendar-heatmap/dist/styles.css";
import LogoutButton from "./LogoutButton";
import ProjectModal from "./ProjectModal";

const Dashboard = () => {
  const [projects, setProjects] = useState([]);
  const [projectIds, setProjectIds] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [filteredProjects, setFilteredProjects] = useState([]);
  const [activities, setActivities] = useState([]);
  const [isModalOpen, setIsModalOpen] = useState(false);

  useEffect(() => {
    const fetchProjects = async () => {
      try {
        const response = await axios.get("/api/projects");
        setProjects(response.data);
        setFilteredProjects(response.data);
        setProjectIds(response.data.map(project => project.id));
      } catch (error) {
        console.error("Error fetching projects:", error);
      }
    };

    const fetchActivities = async () => {
      try {
        const response = await axios.get("/api/activities");
        setActivities(response.data);
      } catch (error) {
        console.error("Error fetching activities:", error);
      }
    };

    fetchProjects();
    fetchActivities();
  }, []);

  const handleSearch = (event) => {
    setSearchTerm(event.target.value);
    const filtered = projects.filter((project) =>
      project.name.toLowerCase().includes(event.target.value.toLowerCase())
    );
    setFilteredProjects(filtered);
  };

  return (
    <div className="bg-gray-100 p-8 min-h-screen relative">
      <div className="absolute top-4 right-4">
        <LogoutButton />
      </div>
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-6 text-center">Dashboard</h1>
        <div className="mb-6 flex justify-between items-center">
          <input
            type="text"
            placeholder="Search projects..."
            value={searchTerm}
            onChange={handleSearch}
            className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            onClick={() => setIsModalOpen(true)}
            className="ml-4 px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-700"
          >
            New Project
          </button>
        </div>
        <div className="mb-6">
          <h2 className="text-2xl font-bold mb-4">Activity Tracker</h2>
          <CalendarHeatmap
            startDate={new Date(new Date().setFullYear(new Date().getFullYear() - 1))}
            endDate={new Date()}
            values={activities}
            classForValue={(value) => {
              if (!value) {
                return "color-empty";
              }
              return `color-scale-${value.count}`;
            }}
            tooltipDataAttrs={(value) => {
              return {
                "data-tip": `${value.date}: ${value.count} activities`,
              };
            }}
          />
        </div>
        <div>
          <h2 className="text-2xl font-bold mb-4">Projects</h2>
          <ul>
            {filteredProjects.map((project) => (
              <li key={project.id} className="mb-4 p-4 bg-white rounded-lg shadow">
                <h3 className="text-xl font-bold">{project.name}</h3>
                <p>{project.description}</p>
                <p className="text-gray-500 text-sm">
                  {new Date(project.updated_at).toLocaleDateString()}
                </p>
              </li>
            ))}
          </ul>
        </div>
      </div>
      <ProjectModal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} projectIds={projectIds} />
    </div>
  );
};

export default Dashboard;