import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import RedirectHandler from './pages/RedirectHandler';

/**
 * WHY a central App.tsx?
 * This is the 'root' of your component tree. We define the global layout
 * (Navbar) and handle routing (which page to show for which URL).
 */
const App: React.FC = () => {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50 flex flex-col">
        {/* Global Navbar */}
        <Navbar />

        {/* Main Content Area */}
        <main className="flex-grow">
          <Routes>
            {/* Home Page: The main URL shortening interface */}
            <Route path="/" element={<Home />} />
            
            {/* Redirect Handler: Captures the shortId and handles redirects */}
            {/* For example: http://localhost:5173/aBcd12 */}
            <Route path="/:shortId" element={<RedirectHandler />} />
          </Routes>
        </main>

        {/* Reusable Footer */}
        <footer className="py-8 bg-secondary text-white text-center">
          <div className="max-w-7xl mx-auto px-6">
            <p className="text-sm opacity-60">
              © {new Date().getFullYear()} Mitly - URL Shortener Project
            </p>
          </div>
        </footer>
      </div>
    </Router>
  );
};

export default App;
