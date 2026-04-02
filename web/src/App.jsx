import { useEffect, useState } from 'react';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';
import './App.css';

function App() {
  const [data, setData] = useState([]);
  const [status, setStatus] = useState("SEARCHING...");
  const [resetting, setResetting] = useState(false);
  const [resetStatus, setResetStatus] = useState(null); // 'ok' | 'error' | null

  const fetchData = async () => {
    try {
      const resStatus = await axios.get('/api/status');
      const dbStatus = resStatus.data.database || resStatus.data.db || "Connected";
      setStatus(dbStatus.includes("Error") ? "CRITICAL" : "STABLE");
      const resHistory = await axios.get('/api/history');
      const historyData = resHistory.data.mass_value || resHistory.data || [];
      setData(historyData.slice(0, 8));
    } catch (err) {
      setStatus("OFFLINE");
    }
  };

  const handleReset = async () => {
    if (!window.confirm('Reset database? This action cannot be undone.')) return;
    setResetting(true);
    setResetStatus(null);
    try {
      await axios.post('/api/reset');
      setData([]);
      setStatus("SEARCHING...");
      setResetStatus('ok');
    } catch (err) {
      setResetStatus('error');
    } finally {
      setResetting(false);
      setTimeout(() => setResetStatus(null), 3000);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="void-bg">
      <div className="void-container">
        <h1 className="void-title">Phoenix A*</h1>
        <div className="glass-panel">
          <div className="status-header">
            <span>TELEMETRY LINK</span>
            <div className="status-indicator">
              <div className={`pulse ${status === "STABLE" ? "connected" : "error"}`} />
              <span style={{ color: status === "STABLE" ? '#00ff41' : '#ff003c' }}>
                {status}
              </span>
            </div>
          </div>
          <div className="log-container">
            <AnimatePresence>
              {data.map((item, i) => (
                <motion.div
                  key={item.id || i}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: 20 }}
                  transition={{ duration: 0.5 }}
                  className="log-item"
                >
                  <span className="log-id">[OBS-{item.id || 'SYS'}]</span>
                  <span className="log-mass">{item.mass || item.data} M☉</span>
                </motion.div>
              ))}
            </AnimatePresence>
          </div>

          <div className="reset-section">
            <button
              className={`reset-btn ${resetting ? 'reset-btn--loading' : ''}`}
              onClick={handleReset}
              disabled={resetting}
            >
              {resetting ? 'RESETTING...' : '⬡ INITIATE SINGULARITY RESET'}
            </button>
            <AnimatePresence>
              {resetStatus && (
                <motion.span
                  className={`reset-msg reset-msg--${resetStatus}`}
                  initial={{ opacity: 0, y: -4 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0 }}
                >
                  {resetStatus === 'ok' ? 'DATABASE WIPED.' : 'RESET FAILED.'}
                </motion.span>
              )}
            </AnimatePresence>
          </div>

        </div>
      </div>
    </div>
  );
}

export default App;
