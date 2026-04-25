import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';

// 确保后端服务正在运行 (http://localhost:8000)
// 启动后端服务的命令: cd backend && uvicorn app.main:app --reload

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);