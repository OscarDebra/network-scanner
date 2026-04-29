/**
 * WelcomeScreen.js
 * Landing screen shown on first load.
 * Displays a scan button and backend health status.
 */
 
import React, { useEffect, useState } from 'react';
import { fetchHealth } from '../api';
import './WelcomeScreen.css';
 
export default function WelcomeScreen({ onScan, scanning }) {
  const [healthy, setHealthy] = useState(null);
 
  useEffect(() => {
    fetchHealth()
      .then(() => setHealthy(true))
      .catch(() => setHealthy(false));
  }, []);
 
  return (
    <div className="welcome">
      <div className="welcome-grid" aria-hidden="true">
        {Array.from({ length: 64 }).map((_, i) => (
          <div key={i} className="grid-cell" />
        ))}
      </div>
 
      <div className="welcome-content">
        <div className="welcome-badge">
          <span className={`status-dot ${healthy === true ? 'online' : healthy === false ? 'offline' : 'checking'}`} />
          <span className="status-label">
            {healthy === null ? 'checking backend...' : healthy ? 'backend online' : 'backend offline'}
          </span>
        </div>
 
        <h1 className="welcome-title">
          <span className="title-line">NETWORK</span>
          <span className="title-line accent">SCANNER</span>
        </h1>
 
        <p className="welcome-subtitle">
          Discover every device on your local network.<br />
          IP addresses, MAC addresses, vendors — all in one place.
        </p>
 
        <button
          className={`scan-btn ${scanning ? 'scanning' : ''}`}
          onClick={onScan}
          disabled={scanning || healthy === false}
        >
          {scanning ? (
            <>
              <span className="scan-spinner" />
              SCANNING...
            </>
          ) : (
            <>
              <span className="scan-icon">▶</span>
              START SCAN
            </>
          )}
        </button>
 
        {healthy === false && (
          <p className="welcome-error">
            Cannot reach backend at /api/health — is the container running?
          </p>
        )}
      </div>
    </div>
  );
}
 