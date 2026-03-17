import React from 'react';
import { Link } from 'react-router-dom';

/**
 * WHY a separate Navbar component?
 * Every professional app reuses its header and footer.
 * If you add more pages later (like 'Analytics' or 'Login'),
 * you only have to update the navigation here once.
 */
const Navbar: React.FC = () => {
  return (
    <nav className="bg-white border-b border-gray-100 py-4 shadow-sm">
      <div className="max-container flex justify-between items-center px-6 mx-auto max-w-7xl">
        <Link to="/" className="flex items-center gap-2">
          {/* We use the logo we copied from backend/media */}
          <img 
            src="/logos/mitly-type-orange.svg" 
            alt="Mitly Logo" 
            className="h-8 md:h-10"
          />
        </Link>
        <div className="flex gap-6 items-center">
          <Link to="/" className="text-gray-600 hover:text-primary font-medium transition-colors">
            Home
          </Link>
          <a 
            href="https://github.com/miray-mustafov/mitly" 
            target="_blank" 
            rel="noopener noreferrer"
            className="text-gray-600 hover:text-primary font-medium transition-colors"
          >
            GitHub
          </a>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
