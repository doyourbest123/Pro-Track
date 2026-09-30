import { useState, useEffect } from 'react';
import StockChart from './components/StockChart';

function App() {
  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [refreshKey, setRefreshKey] = useState(0);

  const fetchDashboard = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await fetch('http://localhost:8000/api/dashboard');
      if (!response.ok) {
        throw new Error('Failed to load dashboard data.');
      }
      const result = await response.json();
      setDashboard(result);
      setRefreshKey((prev) => prev + 1);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Trigger backend market refresh + Gemini AI analysis
  const handleRefresh = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await fetch('http://localhost:8000/api/watchlist/refresh?trigger_ai=true', {
        method: 'POST',
      });
      if (!response.ok) {
        throw new Error('Failed to refresh market data.');
      }
      const result = await response.json();
      setDashboard(result.payload);
      setRefreshKey((prev) => prev + 1);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboard();
  }, []);

  return (
    <div style={{ maxWidth: '800px', margin: '2rem auto', fontFamily: 'sans-serif', padding: '0 1rem' }}>
      <h1>ProTrack - {dashboard?.watchlist_name || 'Stock Dashboard'}</h1>

      <button 
        onClick={handleRefresh} 
        disabled={loading}
        style={{ padding: '10px 16px', marginBottom: '1.5rem', cursor: 'pointer' }}
      >
        {loading ? 'Refreshing & Running AI...' : 'Refresh Market Data & AI'}
      </button>

      {error && <p style={{ color: 'red' }}>{error}</p>}

      {dashboard?.stocks?.map((item) => {
        const metrics = item.market_metrics;
        const ai = metrics?.ai_opinion;
        // Access history array per stock or fall back to item.history
        const historyData = metrics?.history || item.history || dashboard?.history;

        return (
          <div key={item.ticker} style={{ border: '1px solid #ddd', borderRadius: '8px', padding: '1.5rem', marginBottom: '1rem' }}>
            <h2>{metrics?.long_name || item.ticker} ({item.ticker})</h2>
            <p><strong>Price:</strong> ${metrics?.current_price}</p>
            <p><strong>P/E Ratio:</strong> {metrics?.pe_ratio || 'N/A'}</p>

            {historyData && (
              <div style={{ margin: '1.5rem 0' }}>
                <StockChart historyData={historyData} animationKey={refreshKey} />
              </div>
            )}

            <hr style={{ margin: '1rem 0' }} />

            <h3>Gemini AI Analysis</h3>
            {ai ? (
              <ul>
                <li><strong>Valuation:</strong> {ai.valuation_verdict}</li>
                <li><strong>Risk:</strong> {ai.risk_view}</li>
                <li><strong>Profitability:</strong> {ai.profitability_verdict}</li>
              </ul>
            ) : (
              <p>Click refresh to generate AI analysis.</p>
            )}
          </div>
        );
      })}
    </div>
  );
}

export default App;