import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { urlService } from '../services/urlService';

/**
 * WHY a RedirectHandler?
 * This page is responsible for checking if the short ID exists.
 * If it does, it redirects the user to the original long URL.
 * If it doesn't (or is expired), it shows a friendly error message.
 */
const RedirectHandler: React.FC = () => {
  const { shortId } = useParams<{ shortId: string }>();
  const navigate = useNavigate();
  const [status, setStatus] = useState<'loading' | 'error' | 'expired'>('loading');
  const [errorMsg, setErrorMsg] = useState('');

  useEffect(() => {
    const fetchAndRedirect = async () => {
      if (!shortId) return;

      try {
        const data = await urlService.getUrl(shortId);
        
        if (data.is_expired) {
          setStatus('expired');
          return;
        }

        // Redirect the user's browser to the original URL
        window.location.href = data.original_url;
      } catch (err: any) {
        setStatus('error');
        if (err.response?.status === 410) {
          setStatus('expired');
        } else {
          setErrorMsg(err.response?.data?.detail || 'URL not found');
        }
      }
    };

    fetchAndRedirect();
  }, [shortId]);

  if (status === 'loading') {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh]">
        <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-primary mb-4"></div>
        <p className="text-gray-600 font-medium">Redirecting you to your destination...</p>
      </div>
    );
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] text-center px-6">
      <div className="bg-red-50 p-8 rounded-2xl border border-red-100 max-w-md">
        <h2 className="text-3xl font-bold text-red-600 mb-4">
          {status === 'expired' ? 'Link Expired' : 'Oops! Link Not Found'}
        </h2>
        <p className="text-gray-600 mb-8">
          {status === 'expired' 
            ? 'This link has reached its expiration date and is no longer available.' 
            : `The link you're trying to reach doesn't exist or has been removed. ${errorMsg}`}
        </p>
        <button
          onClick={() => navigate('/')}
          className="bg-primary hover:bg-primary-dark text-white font-bold py-3 px-8 rounded-lg transition-all"
        >
          Go Back Home
        </button>
      </div>
    </div>
  );
};

export default RedirectHandler;
