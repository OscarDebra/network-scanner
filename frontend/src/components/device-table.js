/**
 * DeviceTable.js
 * Displays the list of devices found in the most recent scan.
 * Columns ordered by priority: Hostname, Status, IP, MAC, Vendor.
 */
 
import React, { useState } from 'react';
import './device-table.css';
 
export default function DeviceTable({ devices, scanMeta, onRescan, scanning }) {
  const [filter, setFilter] = useState('');
  const [sortKey, setSortKey] = useState('ip');
  const [sortDir, setSortDir] = useState('asc');
 
  const filtered = devices
    .filter(d => {
      const q = filter.toLowerCase();
      return (
        d.hostname?.toLowerCase().includes(q) ||
        d.ip?.includes(q) ||
        d.mac?.toLowerCase().includes(q) ||
        d.vendor?.toLowerCase().includes(q)
      );
    })
    .sort((a, b) => {
      let av = a[sortKey] || '';
      let bv = b[sortKey] || '';
      if (sortKey === 'ip') {
        av = a.ip.split('.').map(n => n.padStart(3, '0')).join('');
        bv = b.ip.split('.').map(n => n.padStart(3, '0')).join('');
      }
      return sortDir === 'asc' ? av.localeCompare(bv) : bv.localeCompare(av);
    });
 
  function toggleSort(key) {
    if (sortKey === key) setSortDir(d => d === 'asc' ? 'desc' : 'asc');
    else { setSortKey(key); setSortDir('asc'); }
  }
 
  function SortIcon({ col }) {
    if (sortKey !== col) return <span className="sort-icon inactive">↕</span>;
    return <span className="sort-icon active">{sortDir === 'asc' ? '↑' : '↓'}</span>;
  }
 
  return (
    <div className="dashboard">
      <header className="dash-header">
        <div className="dash-header-left">
          <h2 className="dash-title">NETWORK SCANNER</h2>
          {scanMeta && (
            <div className="dash-meta">
              <span className="meta-item">
                <span className="meta-label">SUBNET</span>
                <span className="meta-value mono">{scanMeta.subnet}</span>
              </span>
              <span className="meta-divider" />
              <span className="meta-item">
                <span className="meta-label">DEVICES</span>
                <span className="meta-value accent">{devices.length}</span>
              </span>
              <span className="meta-divider" />
              <span className="meta-item">
                <span className="meta-label">SCANNED</span>
                <span className="meta-value mono">{scanMeta.finished_at?.replace('T', ' ')}</span>
              </span>
            </div>
          )}
        </div>
        <div className="dash-header-right">
          <input
            className="search-input"
            placeholder="filter devices..."
            value={filter}
            onChange={e => setFilter(e.target.value)}
          />
          <button
            className={`rescan-btn ${scanning ? 'scanning' : ''}`}
            onClick={onRescan}
            disabled={scanning}
          >
            {scanning ? <><span className="scan-spinner-sm" /> SCANNING...</> : '↺ RESCAN'}
          </button>
        </div>
      </header>
 
      <div className="table-wrap">
        <table className="device-table">
          <thead>
            <tr>
              <th onClick={() => toggleSort('hostname')}>HOSTNAME <SortIcon col="hostname" /></th>
              <th>STATUS</th>
              <th onClick={() => toggleSort('ip')}>IP ADDRESS <SortIcon col="ip" /></th>
              <th onClick={() => toggleSort('mac')}>MAC ADDRESS <SortIcon col="mac" /></th>
              <th onClick={() => toggleSort('vendor')}>VENDOR <SortIcon col="vendor" /></th>
            </tr>
          </thead>
          <tbody>
            {filtered.length === 0 ? (
              <tr>
                <td colSpan={5} className="empty-row">No devices match your filter.</td>
              </tr>
            ) : (
              filtered.map((d, i) => (
                <tr key={d.ip} style={{ animationDelay: `${i * 20}ms` }} className="device-row">
                  <td className="col-hostname">
                    {d.hostname && d.hostname !== 'Unknown'
                      ? <span className="hostname-known">{d.hostname}</span>
                      : <span className="hostname-unknown">—</span>
                    }
                  </td>
                  <td>
                    <span className={`status-badge ${d.status === 'up' ? 'up' : 'down'}`}>
                      {d.status === 'up' ? '● UP' : '○ DOWN'}
                    </span>
                  </td>
                  <td className="mono">{d.ip}</td>
                  <td className="mono col-mac">{d.mac}</td>
                  <td className="col-vendor">
                    {d.vendor && d.vendor !== 'Unknown'
                      ? <span className="vendor-known">{d.vendor}</span>
                      : <span className="vendor-unknown">Unknown</span>
                    }
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
 
      <footer className="dash-footer">
        <span className="mono">{filtered.length} of {devices.length} devices shown</span>
      </footer>
    </div>
  );
}