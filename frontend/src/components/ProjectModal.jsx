import React, { useState } from "react";
import axios from "axios";

const ProjectModal = ({ isOpen, onClose, projectIds }) => {
  const [projectName, setProjectName] = useState("");
  const [projectDescription, setProjectDescription] = useState("");
  const [template, setTemplate] = useState("");
  const [parameters, setParameters] = useState([{ name: "", value: "" }]);

  const handleCreateProject = async () => {
    try {
      const response = await axios.post("/api/projects", {
        name: projectName,
        description: projectDescription,
        parameters: parameters,
      });
      onClose();
    } catch (error) {
      console.error("Error creating project:", error);
    }
  };

  const handleAddParameter = () => {
    setParameters([...parameters, { name: "", value: "" }]);
  };

  const handleRemoveParameter = (index) => {
    const newParameters = parameters.filter((_, i) => i !== index);
    setParameters(newParameters);
  };

  const handleParameterChange = (index, field, value) => {
    const newParameters = parameters.map((param, i) =>
      i === index ? { ...param, [field]: value } : param
    );
    setParameters(newParameters);
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-gray-600 bg-opacity-50 flex justify-center items-center">
      <div className="bg-white p-6 rounded-lg shadow-lg w-full max-w-md max-h-screen overflow-y-auto">
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
          <option value="">No Template</option>
          <option value="neural_network">Neural Network</option>
          <option value="template2">Template 2</option>
        </select>
        <div className="mb-4">
          <h3 className="text-xl font-bold mb-2">Parameters</h3>
          <div className="max-h-80 overflow-y-auto">
            {parameters.map((param, index) => (
              <div key={index} className="flex mb-2">
                <input
                  type="text"
                  placeholder="Name"
                  value={param.name}
                  onChange={(e) => handleParameterChange(index, "name", e.target.value)}
                  className="w-1/2 px-4 py-2 border rounded-l-lg"
                />
                <input
                  type="text"
                  placeholder="Value"
                  value={param.value}
                  onChange={(e) => handleParameterChange(index, "value", e.target.value)}
                  className="w-1/2 px-4 py-2 border rounded-r-lg"
                />
                <button
                  onClick={() => handleRemoveParameter(index)}
                  className="ml-2 px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-700"
                >
                  Remove
                </button>
              </div>
            ))}
          </div>
          <button
            onClick={handleAddParameter}
            className="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-700"
          >
            Add Parameter
          </button>
        </div>
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