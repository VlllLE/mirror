// she broke im up
// app.js
// therapybot v2 
// m@vile.cx

import React, { useState, useEffect } from 'react';
import './App.css';

const themes = ['moonlight', 'light', 'dark'];

function App() {
  const [message, setMessage] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);
  const [theme, setTheme] = useState('moonlight');
  const [user, setUser] = useState('');
  const [showAbout, setShowAbout] = useState(false);
  const [showDisclaimer, setShowDisclaimer] = useState(false);
  const [showDocs, setShowDocs] = useState(false);
  const [showRoadmap, setShowRoadmap] = useState(false);


  useEffect(() => {
    const savedTheme = localStorage.getItem('mirror-theme') || 'moonlight';
    const savedUser = localStorage.getItem('mirror-user') || '';

    setTheme(savedTheme);
    setUser(savedUser);

    const link = document.getElementById('theme-link') || (() => {
      const l = document.createElement('link');
      l.id = 'theme-link';
      l.rel = 'stylesheet';
      document.head.appendChild(l);
      return l;
    })();

    link.href = `${process.env.PUBLIC_URL}/themes/${savedTheme}.css`;
  }, []);

  useEffect(() => {
    localStorage.setItem('mirror-theme', theme);
    const link = document.getElementById('theme-link');
    if (link) link.href = `${process.env.PUBLIC_URL}/themes/${theme}.css`;
  }, [theme]);

  useEffect(() => {
    localStorage.setItem('mirror-user', user);
  }, [user]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!message.trim() || !user.trim()) return;

    setLoading(true);

    const res = await fetch('http://127.0.0.1:5000/reflect', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user, message }),
    });

    const data = await res.json();
    setResponse(data.response);
    setMessage('');
    setLoading(false);
  };

  return (
  <div className="app-wrapper" style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
    
    {/* Main layout: sidebar + content */}
    <div style={{ display: 'flex', flex: 1 }}>
      {/* Sidebar */}
      <div className="sidebar" style={{ minWidth: '250px', padding: '1rem' }}>
        <h2 style={{ fontSize: '1.2rem' }}>mirrorq.ai</h2>

        <label htmlFor="user-input">User:</label>
        <input
          id="user-input"
          type="text"
          value={user}
          onChange={(e) => setUser(e.target.value.trim())}
          placeholder="e.g. wave"
          style={{ marginTop: '0.3rem', padding: '0.3rem', width: '100%' }}
        />

        <label htmlFor="theme-select" style={{ marginTop: '1rem' }}>Theme:</label>
        <select
          id="theme-select"
          value={theme}
          onChange={(e) => setTheme(e.target.value)}
          style={{ marginTop: '0.3rem', padding: '0.3rem', width: '100%' }}
        >
          {themes.map((t) => (
            <option key={t} value={t}>
              {t === "light" ? "Bright" : t.charAt(0).toUpperCase() + t.slice(1)}
            </option>
          ))}
        </select>

        <ul style={{ listStyle: 'none', padding: 0, marginTop: '2rem' }}>
          <li>
            <button onClick={() => setShowAbout(true)} style={{ all: 'unset', cursor: 'pointer', color: 'inherit' }}>
              About
            </button>
          </li>
          <li>
            <button onClick={() => setShowDisclaimer(true)} style={{all: 'unset', cursor: 'pointer', color: 'inherit'}}>
              Disclaimer
            </button>
          </li>
          <li>
            <button onClick={() => setShowDocs(true)} style={{all: 'unset', cursor: 'pointer', color: 'inherit'}}>
              Documents
            </button>
          </li>
          <li>
            <button onClick={() => setShowRoadmap(true)} style={{all: 'unset', cursor: 'pointer', color: 'inherit'}}>
              Roadmap
            </button>
          </li>
        </ul>
      </div>

      {/* Main content */}
      <main className="mirror-container" style={{ flexGrow: 1, padding: '2rem' }}>
        <h1 className="mirror-title">mirror</h1>
        <form className="mirror-form" onSubmit={handleSubmit}>
          <textarea
            rows="4"
            className="mirror-input"
            placeholder="What's on your mind?"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
          />
          <button type="submit" className="mirror-button">Insight</button>
        </form>

        {loading && <p className="mirror-loading">⏳ Reflecting...</p>}
        {response && (
          <div className="mirror-response" style={{ marginTop: '1rem', padding: '1rem', borderRadius: '8px', background: 'rgba(255,255,255,0.05)' }}>
            <strong>mirror:</strong>
            <p>{response}</p>
          </div>
        )}
      </main>
    </div>

    {/* Footer */}
    <footer className="text-center text-sm text-gray-500 p-4">
      <p>
        mirror is a reflective AI tool, not a licensed therapist. If you're in crisis, please seek professional support.
      </p>
      <p className="mt-1">&copy; {new Date().getFullYear()} mirrorq- -m@vile.cx</p>
    </footer>

    {/* About modal */}
    {showAbout && (
     <Modal title="About mirror" onClose={() => setShowAbout(false)}>
    <p><em>mirror</em> is a soft companion designed to help you reflect - gently. It's powered by AI, but shaped with heart. Everything here is <strong>private</strong>, non-judgmental, and crafted to hold emotional space, not offer solutions.</p>
    <p><em>mirror</em> reflects patterns, surfaces quiet biases, and invites gentle self-honesty.</p>
    <p><strong>What it isn't:</strong> <em>mirror</em> is not a licensed therapist or a substitute for real help. If you're in crisis, please reach out to someone trained. Helplines are listed under <em>Disclaimer</em>.</p>
    <p><em>Your reflections stay local</em> - nothing is stored externally. No data leaves your screen.</p>
    <p>If this helps you in any way, I'd love to hear. ~ <a href="mailto:m@vile.cx">m@vile.cx</a></p>
     </Modal>
     
    )}
    {showDisclaimer && (
    <Modal title="Disclaimer" onClose={() => setShowDisclaimer(false)}>
    <p><em>mirror</em> is an introspection tool powered by AI. It is not a licensed therapist or crisis support service.</p>
    <p style={{ marginTop: '1rem' }}>If you are in immediate danger or need urgent help, please contact a mental health professional or crisis line.</p>
    <p><strong>UK</strong>- NHS: 111, Samaritans: 116 123</p>
    <p><strong>US</strong>- Call: <strong>911</strong><em> alternatively,</em> Suicide Hotline: 988</p>
  </Modal>
)}

{showDocs && (
  <Modal title="Documents" onClose={() => setShowDocs(false)}>
    <ul>
      <li><strong>Whitepaper</strong><em>(at some point, probably)</em></li>
      <li><strong>Safety Philosophy</strong> - mirror never diagnoses or judges. It gently reflects.</li>
      <li><strong>Ethics</strong> - tagging, flagging, and interpretive tools aim to reduce bias and promote self-awareness.</li>

    </ul>
  </Modal>
)}

{showRoadmap && (
  <Modal title="Roadmap" onClose={() => setShowRoadmap(false)}>
    <ul>
      <li>Persistent memory - <em>complete</em></li>
      <li>Tag-based introspection - <em>complete</em></li>
      <li>Recursive feedback loop - <em>complete</em></li>
      <li>Launch-ready safety guardrails - <em>complete</em></li>
      <li>Feedback-based tuning</li>
      <li>Themes</li>
      <li>Multiple users</li>
      <li>Settings</li>
      <li>Better models</li>
      <li>Better responses</li>
      <li>Better UI</li>
      <li>Better UX</li>
      <li>Better SEO</li>
      <li>Better performance</li>
      <li>Better security</li>
      <li>Better accessibility</li>
      <li>Better internationalization</li>
      <li>Better localization</li>
    </ul>
  </Modal>
)}
  </div>
);
}

export default App;
function Modal({ title, children, onClose }) {
  return (
    <div style={{
      position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
      background: 'rgba(0, 0, 0, 0.6)', display: 'flex',
      justifyContent: 'center', alignItems: 'center', zIndex: 1000
    }}>
      <div style={{
        background: '#fff', color: '#000', padding: '2rem', borderRadius: '12px',
        maxWidth: '600px', width: '90%', boxShadow: '0 0 20px rgba(0,0,0,0.3)',
        maxHeight: '80vh', overflowY: 'auto'
      }}>
        <h2 style={{ marginTop: 0 }}>{title}</h2>
        <div style={{ marginTop: '1rem' }}>{children}</div>
        <button onClick={onClose} className="mirror-button" style={{ marginTop: '1.5rem' }}>
          Close
        </button>
      </div>
    </div>
  );
}