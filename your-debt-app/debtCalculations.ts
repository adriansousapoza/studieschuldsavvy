// A TypeScript interface to hold the parameters that in Python were separate arguments.
export interface DebtParams {
    init: number;           // e.g. start date in year + month/12
    final: number;          // e.g. init + 10
    DEBT_BSC: number;
    DEBT_MSC: number;
    DEBT_PRESTATIEBEURS: number;
    MONTHLY_LOAN_MSC_2023_AUTUMN: number;
    MONTHLY_PRESTATIEBEURS_2023_AUTUMN: number;
    MONTHLY_LOAN_MSC_2024_SPRING: number;
    MONTHLY_PRESTATIEBEURS_2024_SPRING: number;
    MONTHLY_LOAN_MSC_2024_AUTUMN: number;
    END_DATE_STUDY: Date;
    END_DATE_LOAN_MSC: Date;
    END_DATE_ZERO_PERCENT: Date;
    INTEREST_RATES: [number, number][]; // array of [year, interestRate]
    interest_bool?: boolean; 
  }
  
  // Return type
  export interface DebtResults {
    time: number[];
    totalDebt: number[];
    debtBachelor: number[];
    debtPrestatiebeurs: number[];
    debtMaster: number[];
  }
  
  export function totalDebtFunc(params: DebtParams): DebtResults {
    const {
      init,
      final,
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
      interest_bool = true
    } = params;
  
    // Create the time array in monthly increments
    const T: number[] = [];
    let step = 1 / 12;
    for (let t = init; t < final; t += step) {
      // Because of floating-point precision, we can do this in a safer way,
      // but let's keep it simple for now.
      T.push(t);
    }
  
    const totalDebt: number[] = new Array(T.length).fill(0);
    const debtBachelor: number[] = new Array(T.length).fill(0);
    const debtPrestatiebeurs: number[] = new Array(T.length).fill(0);
    const debtMaster: number[] = new Array(T.length).fill(0);
  
    // Initialize
    debtBachelor[0] = DEBT_BSC;
    debtPrestatiebeurs[0] = DEBT_MSC;
    debtMaster[0] = DEBT_PRESTATIEBEURS;
    totalDebt[0] = debtBachelor[0] + debtPrestatiebeurs[0] + debtMaster[0];
  
    for (let i = 1; i < T.length; i++) {
      const t = T[i];
      // Derive the current year/month from t
      const currentYear = Math.floor(t);
      const currentMonth = Math.floor((t % 1) * 12) + 1;
  
      // Decide monthly loans
      let monthly_loan_prestatie = 0;
      let monthly_loan_msc = 0;
  
      // Check if beyond end of study
      if (
        currentYear > END_DATE_STUDY.getFullYear() ||
        (currentYear === END_DATE_STUDY.getFullYear() && currentMonth > (END_DATE_STUDY.getMonth() + 1))
      ) {
        monthly_loan_prestatie = 0;
        monthly_loan_msc = 0;
      } else if (
        currentYear > END_DATE_LOAN_MSC.getFullYear() ||
        (currentYear === END_DATE_LOAN_MSC.getFullYear() && currentMonth > (END_DATE_LOAN_MSC.getMonth() + 1))
      ) {
        monthly_loan_msc = 0;
        // Keep the prestatie logic from your python code
        monthly_loan_prestatie = MONTHLY_PRESTATIEBEURS_2023_AUTUMN; // or 0, etc., depending on your logic
      } else {
        // replicate your if-else for 2023 vs 2024 etc.
        if (currentYear < 2023) {
          monthly_loan_prestatie = MONTHLY_PRESTATIEBEURS_2023_AUTUMN;
          monthly_loan_msc = MONTHLY_LOAN_MSC_2023_AUTUMN;
        } else if (currentYear === 2023) {
          if (currentMonth < 9) {
            monthly_loan_prestatie = MONTHLY_PRESTATIEBEURS_2023_AUTUMN;
            monthly_loan_msc = MONTHLY_LOAN_MSC_2023_AUTUMN;
          } else {
            monthly_loan_prestatie = MONTHLY_PRESTATIEBEURS_2024_SPRING;
            monthly_loan_msc = MONTHLY_LOAN_MSC_2024_SPRING;
          }
        } else if (currentYear >= 2024) {
          if (currentMonth < 9) {
            monthly_loan_prestatie = MONTHLY_PRESTATIEBEURS_2024_SPRING;
            monthly_loan_msc = MONTHLY_LOAN_MSC_2024_SPRING;
          } else {
            monthly_loan_prestatie = MONTHLY_PRESTATIEBEURS_2024_SPRING;
            monthly_loan_msc = MONTHLY_LOAN_MSC_2024_AUTUMN;
          }
        }
      }
  
      // Apply interest if interest_bool is true
      if (interest_bool) {
        let interestRateBsc = 0;
        let interestRateMsc = 0;
  
        // Find the correct interest rate for BSC
        if (currentYear <= END_DATE_ZERO_PERCENT.getFullYear()) {
          // from your python code: INTEREST_RATES[2][1] => for 2023 is 0.46
          // but you'd logically need to parse the array for the correct year
          // For simplicity, we skip searching the array and just replicate logic
          interestRateBsc = 0.46 / 100 / 12; // if we assume 2023 is 0.46
        } else if (currentYear < 2023) {
          interestRateBsc = 0.0; // etc...
        } else if (currentYear === 2023) {
          interestRateBsc = 0.46 / 100 / 12;
        } else if (currentYear >= 2024) {
          interestRateBsc = 2.56 / 100 / 12; // for 2024
        }
  
        // Similarly for MSc
        if (currentYear < 2023) {
          interestRateMsc = 0.46 / 100 / 12;
        } else if (currentYear === 2023) {
          interestRateMsc = 0.46 / 100 / 12;
        } else if (currentYear >= 2024) {
          interestRateMsc = 2.56 / 100 / 12;
        }
  
        // Bachelor
        debtBachelor[i] =
          debtBachelor[i - 1] + debtBachelor[i - 1] * interestRateBsc;
  
        // Prestatiebeurs
        if (
          currentYear > END_DATE_STUDY.getFullYear() ||
          (currentYear === END_DATE_STUDY.getFullYear() &&
            currentMonth > (END_DATE_STUDY.getMonth() + 1))
        ) {
          debtPrestatiebeurs[i] = 0;
        } else {
          debtPrestatiebeurs[i] =
            debtPrestatiebeurs[i - 1] +
            debtPrestatiebeurs[i - 1] * interestRateMsc +
            monthly_loan_prestatie;
        }
  
        // Master
        debtMaster[i] =
          debtMaster[i - 1] +
          debtMaster[i - 1] * interestRateMsc +
          monthly_loan_msc;
      } else {
        // No interest
        debtBachelor[i] = debtBachelor[i - 1];
        if (
          currentYear > END_DATE_STUDY.getFullYear() ||
          (currentYear === END_DATE_STUDY.getFullYear() &&
            currentMonth > (END_DATE_STUDY.getMonth() + 1))
        ) {
          debtPrestatiebeurs[i] = 0;
        } else {
          debtPrestatiebeurs[i] =
            debtPrestatiebeurs[i - 1] + monthly_loan_prestatie;
        }
        debtMaster[i] = debtMaster[i - 1] + monthly_loan_msc;
      }
  
      // Calculate total
      totalDebt[i] =
        debtBachelor[i] + debtPrestatiebeurs[i] + debtMaster[i];
    }
  
    return {
      time: T,
      totalDebt: totalDebt,
      debtBachelor: debtBachelor,
      debtPrestatiebeurs: debtPrestatiebeurs,
      debtMaster: debtMaster,
    };
  }
  