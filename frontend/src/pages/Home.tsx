import React, { useState } from 'react';
import { urlService } from '../services/urlService';
import { URLRead } from '../types';
import ResultCard from '../components/ResultCard';

/**
 * WHY a separate Home page?
 * This is the 'entry point' of your app. Keeping the main logic here
 * and the specific UI parts in 'components' keeps the code clean.
 */
const Home: React.FC = () => {
  const [longUrl, setLongUrl] = useState('');
  const [expiryDays, setExpiryDays] = useState<number | ''>('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<URLRead | null>(null);

  /**
   * WHY async/await?
   * Calling an API takes time. 'async' tells React we will wait for a response.
   * 'try/catch' is crucial for professional error handling - if the backend is down,
   * our app shouldn't just crash.
   */
  const handleShorten = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      const data = await urlService.shorten({
        original_url: longUrl,
        expiry_days: expiryDays === '' ? undefined : expiryDays,
      });
      setResult(data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Something went wrong. Please check your URL.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center py-16 px-6 max-w-4xl mx-auto">
      <div className="text-center mb-12">
        <h1 className="text-4xl md:text-5xl font-extrabold text-secondary mb-4 leading-tight">
          Build stronger digital connections
        </h1>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto">
          Use our URL shortener to create a shortened link making it easy to share.
        </p>
      </div>

      <div className="w-full bg-white rounded-xl shadow-xl p-8 border border-gray-100 mb-8">
        <form onSubmit={handleShorten} className="flex flex-col gap-6">
          <div className="flex flex-col gap-2">
            <label htmlFor="url" className="text-sm font-semibold text-gray-700">
              Shorten a long link
            </label>
            <input
              id="url"
              type="url"
              required
              placeholder="Example: http://super-long-link.com/very/long/path"
              className="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent outline-none transition-all text-gray-800"
              value={longUrl}
              onChange={(e) => setLongUrl(e.target.value)}
            />
          </div>

          <div className="flex flex-col gap-2">
            <label htmlFor="expiry" className="text-sm font-semibold text-gray-700">
              Expiration Days (Optional, 1-365)
            </label>
            <input
              id="expiry"
              type="number"
              min="1"
              max="365"
              placeholder="e.g. 7"
              className="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent outline-none transition-all text-gray-800"
              value={expiryDays}
              onChange={(e) => setExpiryDays(e.target.value === '' ? '' : parseInt(e.target.value))}
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className={`w-full py-4 rounded-lg font-bold text-lg text-white transition-all
              ${loading 
                ? 'bg-gray-400 cursor-not-allowed' 
                : 'bg-primary hover:bg-primary-dark shadow-lg hover:shadow-primary/30 active:scale-[0.98]'
              }`}
          >
            {loading ? 'Shortening...' : 'Shorten it!'}
          </button>
        </form>

        {error && (
          <div className="mt-6 p-4 bg-red-50 border-l-4 border-red-500 text-red-700 animate-pulse">
            {error}
          </div>
        )}
      </div>

      {result && <ResultCard result={result} />}
    </div>
  );
};

export default Home;
