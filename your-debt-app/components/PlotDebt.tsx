import React from 'react';
import Plot from 'react-plotly.js';

interface PlotDebtProps {
  time: number[];
  totalDebtWithInterest: number[];
  totalDebtWithoutInterest: number[];
  xEnd: number;
}

const PlotDebt: React.FC<PlotDebtProps> = ({
  time,
  totalDebtWithInterest,
  totalDebtWithoutInterest,
  xEnd,
}) => {
  const maxY = Math.max(...totalDebtWithInterest, ...totalDebtWithoutInterest);

  return (
    <Plot
      data={[
        {
          x: time,
          y: totalDebtWithInterest,
          type: 'scatter',
          mode: 'lines',
          name: 'With Interest',
        },
        {
          x: time,
          y: totalDebtWithoutInterest,
          type: 'scatter',
          mode: 'lines',
          name: 'Without Interest',
        },
        {
          x: [xEnd, xEnd],
          y: [0, maxY],
          mode: 'lines',
          line: { dash: 'dash', color: 'red' },
          name: 'End Study',
        },
      ]}
      layout={{
        title: 'Total Debt',
        xaxis: { title: 'Year' },
        yaxis: { title: 'Euros' },
      }}
      style={{ width: '100%', height: '500px' }}
    />
  );
};

export default PlotDebt;
