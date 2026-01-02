import React from 'react';
import './Navigation.css';

function Navigation({ currentPage, setCurrentPage }) {
  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: '📊' },
    { id: 'correlation', label: 'Correlation', icon: '🔗' },
    { id: 'attack-chains', label: 'Attack Chains', icon: '⛓️' },
    { id: 'logs', label: 'Logs', icon: '📋' },
    { id: 'alerts', label: 'Alerts', icon: '🚨' },
  ];

  return (
    <nav className="navigation">
      <div className="nav-container">
        {navItems.map((item) => (
          <button
            key={item.id}
            className={`nav-item ${currentPage === item.id ? 'active' : ''}`}
            onClick={() => setCurrentPage(item.id)}
          >
            <span className="nav-icon">{item.icon}</span>
            <span className="nav-label">{item.label}</span>
          </button>
        ))}
      </div>
    </nav>
  );
}

export default Navigation;
