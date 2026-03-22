import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { ShieldAlert, Zap, Utensils, Activity } from 'lucide-react';

function App() {
  const [alerts, setAlerts] = useState([]);
  const [savings, setSavings] = useState({ energy: 1250, food: 15.4 });

  // Sync with your Node.js server (Port 5000)
  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await axios.get('http://localhost:5000/api/alerts');
        setAlerts(res.data);
      } catch (err) {
        console.log("Waiting for server...");
      }
    };
    fetchData();
    const interval = setInterval(fetchData, 3000); // Refresh every 3 seconds
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ backgroundColor: '#0f172a', color: 'white', minHeight: '100vh', padding: '40px', fontFamily: 'sans-serif' }}>
      <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid #1e293b', paddingBottom: '20px' }}>
        <h1 style={{ margin: 0 }}>Kuriftu <span style={{ color: '#4ade80' }}>Omni-Sync</span></h1>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <Activity color="#4ade80" size={20} />
          <span style={{ color: '#94a3b8' }}>System Online</span>
        </div>
      </header>

      {/* KPI Section */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '25px', marginTop: '30px' }}>
        <div style={{ background: '#1e293b', padding: '25px', borderRadius: '15px', boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)' }}>
          <Zap color="#4ade80" size={32} />
          <h3 style={{ color: '#94a3b8', marginTop: '15px' }}>Energy Saved</h3>
          <p style={{ fontSize: '2rem', fontWeight: 'bold', margin: '5px 0' }}>{savings.energy} <span style={{ fontSize: '1rem' }}>ETB</span></p>
        </div>
        <div style={{ background: '#1e293b', padding: '25px', borderRadius: '15px', boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)' }}>
          <Utensils color="#fbbf24" size={32} />
          <h3 style={{ color: '#94a3b8', marginTop: '15px' }}>Food Waste Saved</h3>
          <p style={{ fontSize: '2rem', fontWeight: 'bold', margin: '5px 0' }}>{savings.food} <span style={{ fontSize: '1rem' }}>kg</span></p>
        </div>
      </div>

      {/* Alerts Section */}
      <div style={{ marginTop: '50px' }}>
        <h2 style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <ShieldAlert color="#f87171" /> Guest Requests & Alerts
        </h2>
        
        <div style={{ marginTop: '20px' }}>
          {alerts.length === 0 ? (
            <div style={{ border: '2px dashed #1e293b', padding: '40px', textAlign: 'center', borderRadius: '15px', color: '#64748b' }}>
              No active alerts. Operational efficiency at 100%.
            </div>
          ) : (
            alerts.map((alert) => (
              <div key={alert.id} style={{ background: '#7f1d1d', padding: '20px', borderRadius: '12px', marginBottom: '15px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                  <strong style={{ fontSize: '1.2rem' }}>{alert.room}</strong>
                  <p style={{ margin: '5px 0 0 0', opacity: 0.9 }}>{alert.issue}</p>
                </div>
                <span style={{ fontSize: '0.8rem', opacity: 0.7 }}>{new Date(alert.timestamp).toLocaleTimeString()}</span>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}

export default App;