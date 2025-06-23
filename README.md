# 💼 LBO & DCF Valuation Suite

A modern, interactive web application for advanced financial modeling, including Discounted Cash Flow (DCF) and Leveraged Buyout (LBO) analysis. Built with Streamlit, this tool is designed for finance professionals, students, and anyone interested in company valuation, deal structuring, and financial education.

---

## 🌟 Features at a Glance

- **📈 DCF Engine:** Project and discount free cash flows to estimate intrinsic value.
- **💣 LBO Engine:** Model leveraged buyouts, debt schedules, and investor returns.
- **📊 Growth Simulator:** Visualize different growth scenarios for business value.
- **📅 Debt Forecast:** Analyze debt amortization and repayment schedules.
- **🎨 Modern UI:** Neon/dark theme, interactive charts, and intuitive controls.

---

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Set up Polygon.io API key:**
   - Add your API key to `.streamlit/secrets.toml`:
     ```toml
     POLYGON_API_KEY = "YOUR_API_KEY_HERE"
     ```
   - If you don't have an API key, the app will use demo data.
3. **Run the app:**
   ```bash
   streamlit run app.py
   ```
4. **Open your browser:**
   - Go to [http://localhost:8501](http://localhost:8501)

---

## 📊 Discounted Cash Flow (DCF) Engine

### What is DCF?
Discounted Cash Flow (DCF) is a core valuation method that estimates the value of an investment based on its expected future cash flows, discounted to present value. It is widely used in equity research, investment banking, and corporate finance.

### DCF Steps in the App
1. **Project Free Cash Flows (FCF):**
   - Revenue is grown at a user-defined rate.
   - EBITDA is calculated using a margin assumption.
   - FCF is estimated as a percentage of EBITDA (simplified for demo).
2. **Terminal Value:**
   - Calculated using an exit multiple (e.g., 8x EBITDA) or Gordon Growth Model.
3. **Discounting:**
   - All projected FCFs and terminal value are discounted to present value using the discount rate (WACC).
4. **Enterprise Value (EV):**
   - Sum of discounted FCFs and discounted terminal value.
5. **Equity Value:**
   - EV minus net debt (if data available).

### Key DCF Concepts
- **Free Cash Flow (FCF):** Cash available to all capital providers after operating expenses and investments. FCF = EBITDA - CapEx - ΔWorking Capital - Taxes.
- **EBITDA:** Earnings before interest, taxes, depreciation, and amortization. Proxy for operating cash flow.
- **Discount Rate (WACC):** Weighted Average Cost of Capital. Reflects the required return for all capital providers (debt and equity).
- **Terminal Value:** Value of the business beyond the projection period. Can be a large portion of total value.
- **Exit Multiple:** A market-based multiple (e.g., 8x EBITDA) applied to the final year's EBITDA.
- **Gordon Growth Model:** Terminal value = Final FCF × (1 + g) / (r - g), where g = perpetual growth, r = discount rate.
- **Net Present Value (NPV):** The sum of all future cash flows discounted to today.

#### 📚 Example DCF Calculation
Suppose:
- Year 1 FCF: $10M, grows at 8% per year for 5 years
- Discount rate: 10%
- Terminal value: 8x Year 5 FCF

![NPV Formula](https://latex.codecogs.com/svg.image?NPV%20%3D%20%5Csum_%7Bt%3D1%7D%5E5%20%5Cfrac%7BFCF_t%7D%7B%281%20%2B%20r%29%5Et%7D%20%2B%20%5Cfrac%7BTV%7D%7B%281%20%2B%20r%29%5E5%7D)

---

## 💣 Leveraged Buyout (LBO) Engine

### What is an LBO?
A Leveraged Buyout (LBO) is the acquisition of a company using a significant amount of borrowed money (debt) to meet the purchase price. The assets of the company being acquired, along with those of the acquiring entity, are often used as collateral for the loans. LBOs are a staple of private equity investing.

### LBO Steps in the App
1. **Purchase Price Calculation:**
   - Based on a multiple of EBITDA.
2. **Capital Structure:**
   - User sets the percentage of debt vs. equity.
3. **Debt Schedule:**
   - Debt is amortized over the holding period with interest payments.
4. **Exit Value:**
   - Calculated using an exit multiple on projected EBITDA at exit.
5. **Returns Calculation:**
   - **IRR (Internal Rate of Return):** The annualized effective compounded return rate.
   - **MOIC (Multiple on Invested Capital):** Total cash returned divided by equity invested.

### Key LBO Concepts
- **Leverage:** Use of borrowed funds to increase potential returns (and risk).
- **Equity Invested:** Portion of the purchase price funded by investors.
- **Debt Amortization:** Scheduled repayment of principal over time.
- **IRR:** The discount rate that makes the net present value (NPV) of all cash flows from a particular project equal to zero.
- **MOIC:** Measures how many times the original investment is returned.
- **Debt Service:** Total amount required to cover repayment of interest and principal.
- **Cash Sweep:** Using excess cash flow to pay down debt faster (not modeled in this demo, but common in real LBOs).
- **Entry/Exit Multiple Arbitrage:** Buying at a lower multiple and selling at a higher multiple increases returns.

#### 📚 Example LBO Calculation
Suppose:
- Purchase price: $100M (8x EBITDA)
- Debt: 60% ($60M), Equity: 40% ($40M)
- Debt amortized over 5 years, interest 5%
- Exit at 8x EBITDA, EBITDA grows 8% per year
- Calculate annual cash flows, IRR, and MOIC

---

## 📈 Growth Simulator

- Simulate and visualize different growth scenarios (bear, base, bull cases).
- Adjust growth rates and projection years to see impact on business value.
- Useful for sensitivity analysis and scenario planning.

---

## 📅 Debt Forecast

- Visualize annual debt balances, principal and interest payments.
- Waterfall charts and tables for clear understanding of debt amortization.
- See how leverage decreases over time and how it impacts returns.

---

## 🧮 Math & Finance Concepts Explained

### Present Value (PV)
The value today of a future sum of money, discounted at a specific rate.

![PV Formula](https://latex.codecogs.com/svg.image?PV%20%3D%20%5Cfrac%7BFV%7D%7B%281%20%2B%20r%29%5En%7D)
- FV = Future Value
- r = Discount rate per period
- n = Number of periods

### Net Present Value (NPV)
The sum of all future cash flows (inflows and outflows) discounted to today.

![NPV Formula](https://latex.codecogs.com/svg.image?NPV%20%3D%20%5Csum_%7Bt%3D0%7D%5EN%20%5Cfrac%7BCF_t%7D%7B%281%20%2B%20r%29%5Et%7D)
- CF<sub>t</sub> = Cash flow at time t
- N = Number of periods

### Internal Rate of Return (IRR)
The discount rate that makes the NPV of all cash flows from a project zero. Used to measure investment performance.

![IRR Formula](https://latex.codecogs.com/svg.image?0%20%3D%20%5Csum_%7Bt%3D0%7D%5EN%20%5Cfrac%7BCF_t%7D%7B%281%20%2B%20IRR%29%5Et%7D)

### Weighted Average Cost of Capital (WACC)
The average rate that a company is expected to pay to finance its assets, weighted by the proportion of debt and equity.

![WACC Formula](https://latex.codecogs.com/svg.image?WACC%20%3D%20%5Cfrac%7BE%7D%7BV%7D%20r_e%20%2B%20%5Cfrac%7BD%7D%7BV%7D%20r_d%20%281%20-%20T%29)
- E = Market value of equity
- D = Market value of debt
- V = Total value (E + D)
- r<sub>e</sub> = Cost of equity
- r<sub>d</sub> = Cost of debt
- T = Tax rate

### Terminal Value (TV)
Represents the value of a business beyond the forecast period.

- **Exit Multiple Method:**
  
  ![TV Exit Multiple](https://latex.codecogs.com/svg.image?TV%20%3D%20EBITDA_%7Bfinal%7D%20%5Ctimes%20Exit%20Multiple)

- **Gordon Growth Method:**
  
  ![TV Gordon Growth](https://latex.codecogs.com/svg.image?TV%20%3D%20%5Cfrac%7BFCF_%7Bfinal%7D%20%5Ctimes%20%281%20%2B%20g%29%7D%7Br%20-%20g%7D)
  - g = Perpetual growth rate
  - r = Discount rate

### Debt Amortization
Paying off debt over time in regular installments of principal and interest. In LBOs, this reduces risk and increases equity value over time.

### EBITDA Margin
![EBITDA Margin](https://latex.codecogs.com/svg.image?EBITDA%20Margin%20%3D%20%5Cfrac%7BEBITDA%7D%7BRevenue%7D)
A measure of operating profitability.

### Free Cash Flow (FCF)
![FCF Formula](https://latex.codecogs.com/svg.image?FCF%20%3D%20EBITDA%20-%20CapEx%20-%20%5CDelta%20Working%20Capital%20-%20Taxes)
Represents cash available to all capital providers.

### Multiple on Invested Capital (MOIC)
![MOIC Formula](https://latex.codecogs.com/svg.image?MOIC%20%3D%20%5Cfrac%7BTotal%20Cash%20Returned%7D%7BEquity%20Invested%7D)
A simple measure of investment return.

---

## 🛠️ File Structure

```text
LBODCFmodel/
├── app.py                  # Main Streamlit app
├── requirements.txt        # Python dependencies
├── modules/
│   ├── dcf.py              # DCF logic and display
│   ├── lbo.py              # LBO logic and display
│   ├── growth_simulator.py # Growth simulation logic
│   ├── polygon_api.py      # Data fetching from Polygon.io
│   └── utils.py            # Helper functions and styling
├── .streamlit/
│   ├── config.toml         # Streamlit config
│   └── secrets.toml        # API keys (not tracked in git)
└── README.md               # This file
```

---

## ✨ Customization & Extensibility
- **Add new modules** for other valuation methods (e.g., comparables, M&A).
- **Integrate more data sources** by extending `polygon_api.py`.
- **Enhance UI** with more charts, tabs, and export options.
- **Educational Mode:** Add more tooltips and explanations for learning.

---

## 🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 📚 Further Reading & Resources
- [Aswath Damodaran on Valuation](http://pages.stern.nyu.edu/~adamodar/)
- [Investopedia: DCF](https://www.investopedia.com/terms/d/dcf.asp)
- [Investopedia: LBO](https://www.investopedia.com/terms/l/leveragedbuyout.asp)
- [Polygon.io API Docs](https://polygon.io/docs)
- [Wall Street Prep: LBO Modeling](https://www.wallstreetprep.com/knowledge/leveraged-buyout-lbo/)
- [Corporate Finance Institute: DCF](https://corporatefinanceinstitute.com/resources/valuation/dcf-model-training/)

---

## 📝 License
MIT License. See [LICENSE](LICENSE) for details. 