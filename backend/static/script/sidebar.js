import React from 'react';
import { slide as Menu } from 'react-burger-menu';

export default function Sidebar() {
  return (
    <Menu>
      <a className="menu-item" href="/projects">
        Projects
      </a>
      <a className="menu-item" href="/logout">
        Logout
      </a>
    </Menu>
  );
}