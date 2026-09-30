import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

export default function StockChart({ historyData, animationKey }) {
  const hasData = Array.isArray(historyData) && historyData.length > 0;

  if (!hasData) {
    return (
      <div style={{ color: '#888', fontStyle: 'italic', padding: '1rem 0' }}>
        No historical chart data available.
      </div>
    );
  }

  return (
    <div style={{ width: '100%', height: 250, minHeight: 250 }}>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={historyData} key={animationKey}>
          <XAxis dataKey="date" stroke="#888" />
          <YAxis domain={['auto', 'auto']} stroke="#888" />
          <Tooltip contentStyle={{ backgroundColor: '#222', borderRadius: '4px', border: '1px solid #444' }} />
          <Line
            type="monotone"
            dataKey="price"
            stroke="#8884d8"
            strokeWidth={2}
            dot={false}
            isAnimationActive={true}
            animationDuration={1500}
            animationEasing="ease-in-out"
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}