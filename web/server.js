const express = require('express');
const path = require('path');
const { createProxyMiddleware } = require('http-proxy-middleware');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 5173; // Dev server port

// Allow CORS for local testing
app.use(cors());

// Serve static files
app.use(express.static(path.join(__dirname, 'public')));

// Proxy to Python Flask chatbot_unified.py
// Adjust target below if your Flask port differs (default 5000)
const FLASK_PORT = process.env.FLASK_PORT || 5000;
const FLASK_HOST = process.env.FLASK_HOST || 'http://localhost:' + FLASK_PORT;

// Example endpoints expected from chatbot_unified.py
// - POST /api/chat { message }
// - Optional: /api/yacht/preview-parts, /api/yacht/register-selected
app.use('/api', createProxyMiddleware({
  target: FLASK_HOST,
  changeOrigin: true,
  // For development, log proxying
  onProxyReq(proxyReq, req, res) {
    console.log(`[proxy] ${req.method} ${req.originalUrl} -> ${FLASK_HOST}${req.originalUrl}`);
  },
}));

// Fallback to index.html
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.listen(PORT, () => {
  console.log(`Web UI running at http://localhost:${PORT}`);
  console.log(`Proxying /api/* to ${FLASK_HOST}`);
});
