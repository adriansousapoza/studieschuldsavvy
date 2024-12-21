import React, { useState, useEffect } from 'react';
import PlotDebt from '../components/PlotDebt';
import { totalDebtFunc } from '../debtCalculations';

const HomePage: React.FC = () => {
  // For demonstration, define your parameters here or fetch them from an API
  const [time, setTime] = useState<number[]>([]);
  const [totalDebtWithInterest, setTotalDebtWithInterest] = useState<number[]>([]);
  const [totalDebtWithoutInterest, setTotalDebtWithoutInterest] = useState<number[]>([]);
  const [xEnd, setXEnd] = useState<number>(0);

  useEffect(() => {
    // Hard-coded example of all your parameters:
    const DEBT_BSC = 41899.78;
    const DEBT_MSC = 2406.86 + 11903.13;
    const DEBT_PRESTATIEBEURS = 439.20 + 1509.43;
    const MONTHLY_LOAN_MSC_2023_AUTUMN = 682.97 + 192.83;
    const MONTHLY_PRESTATIEBEURS_2023_AUTUMN = 120.96 + 439.20;
    const MONTHLY_LOAN_MSC_2024_SPRING = 751.27 + 192.83;
    const MONTHLY_PRESTATIEBEURS_2024_SPRING = 466.69 + 120.96;
    const MONTHLY_LOAN_MSC_2024_AUTUMN = 751.27 + 210.83;

    const END_DATE_STUDY = new Date(2024, 9, 31); // 9 => October (0-based)
    const END_DATE_LOAN_MSC = new Date(2023, 11, 31);
    const END_DATE_ZERO_PERCENT = new Date(2026, 11, 31);
    
    // Example interest rates
    const INTEREST_RATES: [number, number][] = [
      [2025, 2.57],
      [2024, 2.56],
      [2023, 0.46],
      [2022, 0.0],
    ];

    const today = new Date();
    const initYear = today.getFullYear() + today.getMonth()/12;
    const final = initYear + 10;
    const xEndVal = END_DATE_STUDY.getFullYear() + (END_DATE_STUDY.getMonth()+1)/12;

    const params = {
      init: initYear,
      final: final,
      DEBT_BSC,
      DEBT_MSC,
      DEBT_PRESTATIEBEURS,
      MONTHLY_LOAN_MSC_2023_AUTUMN,
      MONTHLY_PRESTATIEBEURS_2023_AUTUMN,
      MONTHLY_LOAN_MSC_2024_SPRING,
      MONTHLY_PRESTATIEBEURS_2024_SPRING,
      MONTHLY_LOAN_MSC_2024_AUTUMN,
      END_DATE_STUDY,
      END_DATE_LOAN_MSC,
      END_DATE_ZERO_PERCENT,
      INTEREST_RATES,
      interest_bool: true
    };

    // Debt with interest
    const res1 = totalDebtFunc(params);

    // Debt without interest
    const res2 = totalDebtFunc({ ...params, interest_bool: false });

    setTime(res1.time);
    setTotalDebtWithInterest(res1.totalDebt);
    setTotalDebtWithoutInterest(res2.totalDebt);
    setXEnd(xEndVal);
  }, []);

  return (
    <div>
      <h1>Dutch Student Debt Simulation</h1>
      <PlotDebt
        time={time}
        totalDebtWithInterest={totalDebtWithInterest}
        totalDebtWithoutInterest={totalDebtWithoutInterest}
        xEnd={xEnd}
      />
    </div>
  );
};

export default HomePage;
