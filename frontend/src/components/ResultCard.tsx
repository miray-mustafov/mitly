import React, { useState } from 'react';
import { URLRead } from '../types';

interface Props {
  result: URLRead;
}

const ResultCard: React.FC<Props> = ({ result }) => {
  const [copied, setCopied] = useState(false);

  // We use the current window origin so the link works correctly
  const shortUrl = `${window.location.origin}/${result.short_url_id}`;

  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(shortUrl);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy!', err);
    }
  };

  return (
    <div className="w-full bg-orange-50 rounded-xl p-6 border border-primary/20 flex flex-col md:flex-row items-center justify-between gap-4 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <div className="flex flex-col gap-1 overflow-hidden w-full">
        <span className="text-sm font-medium text-primary">Your shortened URL:</span>
        <a 
          href={shortUrl} 
          target="_blank" 
          rel="noopener noreferrer"
          className="text-xl font-bold text-secondary hover:text-primary transition-colors truncate"
        >
          {shortUrl}
        </a>
        <span className="text-xs text-gray-500 truncate mt-1">
          Redirects to: {result.original_url}
        </span>
      </div>

      <button
        onClick={copyToClipboard}
        className={`whitespace-nowrap px-8 py-3 rounded-lg font-bold transition-all flex items-center gap-2
          ${copied 
            ? 'bg-green-500 text-white' 
            : 'bg-white text-primary border-2 border-primary hover:bg-primary hover:text-white'
          }`}
      >
        {copied ? (
          <>
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
            </svg>
            Copied!
          </>
        ) : 'Copy URL'}
      </button>
    </div>
  );
};

export default ResultCard;
