import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './index.css'

/**
 * WHY a main.tsx?
 * This is the very first file that the browser runs.
 * It grabs the <div id="root"> from your index.html and
 * 'mounts' your entire React app inside it.
 */
ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
