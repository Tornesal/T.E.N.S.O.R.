import React, { useState } from "react";
import axios from "axios";

const ProjectModal = ({ isOpen, onClose }) => {
  const [projectName, setProjectName] = useState("");
  const [projectDescription, setProjectDescription] = useState("");
  const [template, setTemplate] = useState("");

  const handleCreateProject = async () => {
    try {
      const response = await axios.post("/api/projects", {
        name: projectName,
        description: projectDescription,
        template: template,
      });
      //console.log("Project created:", response.data);
      onClose();
    } catch (error) {
      console.error("Error creating project:", error);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-gray-600 bg-opacity-50 flex justify-center items-center">
      <div className="bg-white p-6 rounded-lg shadow-lg">
        <h2 className="text-2xl font-bold mb-4">Create New Project</h2>
        <input
          type="text"
          placeholder="Project Name"
          value={projectName}
          onChange={(e) => setProjectName(e.target.value)}
          className="w-full px-4 py-2 mb-4 border rounded-lg"
        />
        <textarea
          placeholder="Project Description"
          value={projectDescription}
          onChange={(e) => setProjectDescription(e.target.value)}
          className="w-full px-4 py-2 mb-4 border rounded-lg"
        />
        <select
          value={template}
          onChange={(e) => setTemplate(e.target.value)}
          className="w-full px-4 py-2 mb-4 border rounded-lg"
        >
          <option value="">Select Template</option>
          <option value="template1">Template 1</option>
          <option value="template2">Template 2</option>
        </select>
        <div className="flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 bg-gray-500 text-white rounded-lg mr-2"
          >
            Cancel
          </button>
          <button
            onClick={handleCreateProject}
            className="px-4 py-2 bg-blue-500 text-white rounded-lg"
          >
            Create
          </button>
        </div>
      </div>
    </div>
  );
};

export default ProjectModal;