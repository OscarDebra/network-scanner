/**
 * App.js
 * Root component. Manages app state and switches between
 * the WelcomeScreen and DeviceTable views.
 *
 * States:
 *  - welcome:   initial screen, no scan done yet
 *  - scanning:  scan in progress
 *  - results:   scan complete, showing device table
 *  - error:     scan failed
 */
 
import React, { useState } from 'react';
import WelcomeScreen from './components/WelcomeScreen';
import DeviceTable from './components/DeviceTable';
import { fetchScan } from './api';
 
export default function App() {
  const [view, setView] = useState('welcome');
  const [devices, setDevices] = useState([]);
  const [scanMeta, setScanMeta] = useState(null);
  const [error, setError] = useState(null);
 
  async function handleScan() {
    setView('scanning');
    setError(null);
    try {
      const data = await fetchScan();
      if (!data.success) throw new Error(data.error || 'Scan failed');
      setDevices(data.devices);
      setScanMeta({
        subnet: '172.31.0.0/23',
        finished_at: data.devices[0]?.scanned_at || new Date().toISOString(),
        count: data.count
      });
      setView('results');
    } catch (err) {
      setError(err.message);
      setView('error');
    }
  }
 
  if (view === 'welcome' || view === 'scanning') {
    return (
      <WelcomeScreen
        onScan={handleScan}
        scanning={view === 'scanning'}
      />
    );
  }
 
  if (view === 'error') {
    return (
      <WelcomeScreen
        onScan={handleScan}
        scanning={false}
        error={error}
      />
    );
  }
 
  return (
    <DeviceTable
      devices={devices}
      scanMeta={scanMeta}
      onRescan={handleScan}
      scanning={view === 'scanning'}
    />
  );
}
 