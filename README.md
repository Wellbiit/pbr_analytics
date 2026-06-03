# PBR Analytics - Data Analytics Project

## Research Question
**"What factors define success in PBR - stability, career path, or ride quality?"**

## 📊 Tableau Dashboard
🔗 [View Interactive Dashboard on Tableau Public](https://public.tableau.com/app/profile/ann.lutsenko/viz/PBR_17794526682620/PBR)

---

## 📁 Project Structure
```
PBR_Analytics/
│
├── data/
│   ├── cleaned/
│   │   └── riders_2020-2026_clean.csv    # Cleaned dataset
│   ├── raw/
│   │   ├── 2020/                         # Raw scraped data by year
│   │   ├── 2021/
│   │   ├── 2022/
│   │   ├── 2023/
│   │   ├── 2024/
│   │   ├── 2025/
│   │   └── 2026/
│   ├── riders_for_tableau.csv            # Full dataset for Tableau
│   ├── stability.csv                     # Rider stability metrics
│   ├── tour_springboard.csv              # Last tour before UTB debut
│   └── years_to_utb.csv                  # Years to reach UTB
│
├── sql/
│   └── sql.py                            # SQL queries and DB upload
│
├── visuals/
│   ├── prize_vs_score.png
│   ├── stability.png
│   ├── top5_riders.png
│   ├── top10_riders.png
│   ├── tour_avg_ride%.png
│   ├── tour_springboard.png
│   ├── tour_trends.png
│   └── years_to_utb.png
│
├── cleaning.py                           # Data cleaning and transformation
├── scraping.py                           # Web scraping from pbr.com
├── visualization.py                      # Matplotlib charts + CSV export
└── README.md
```

---

## 🛠️ Tech Stack
| Tool | Purpose |
|------|---------|
| Python (pandas, matplotlib, sqlalchemy) | Data collection, cleaning, visualization |
| PostgreSQL + pgAdmin | Data storage, SQL analysis |
| Tableau Public | Interactive dashboards |
| GitHub | Version control |

---

## 📦 Data
- **Source:** pbr.com (web scraping)
- **Period:** 2020-2026
- **Tours:** 7 (Touring Pro Division → Unleash The Best)
- **Rows:** 11,068
- **Columns:** rider, points, avg_score, prize_$, outs, rides, ride_%, tour, year

**Tour hierarchy (low → high):**
`Touring Pro Division` → `Challenger Series` → `PBR Australia/Brazil/Canada` → `Pendleton Whisky Velocity Tour` → `Unleash The Best`

---

## 🔍 Analysis & Key Insights

### 1. Top Riders (2020-2026)
Brady Fielder leads with 5,572 total points, followed by Nick Tetz (5,323) and Dakota Buttar (5,288). The top performers consistently competed across multiple tours and years.

![Top 10 Riders](visuals/top10_riders.png)

---

### 2. Career Path to UTB
To identify the true springboard to the elite Unleash The Best tour, I analyzed the **last tour each rider competed in before their UTB debut** (excluding riders already in UTB in 2020, and accounting for the Challenger Series only existing from 2022).

| Tour | Riders |
|------|--------|
| Touring Pro Division | 56 |
| Challenger Series | 49 |
| Pendleton Whisky Velocity Tour | 23 |
| PBR Brazil | 13 |
| PBR Canada | 12 |
| PBR Australia | 1 |

**Key insight:** TPD remains the primary feeder to UTB. However, the Challenger Series (launched 2022) reached nearly the same numbers in just 4 years, showing its growing importance as an elite pipeline.

**50% of riders reach UTB within just 1 year** of joining PBR (based on 2020-2026 data; riders who debuted in UTB before 2020 are not captured in this analysis).

![Springboard](visuals/tour_springboard.png)
![Years to UTB](visuals/years_to_utb.png)

---

### 3. Ride Quality vs. Prize Money
The scatter plot shows Prize Money vs Average Score per rider (2020-2026). Riders with avg score below 75 earn near-zero prize money regardless of other factors. Above 75, earnings grow but with high variance, suggesting that **ride quality is a necessary but not sufficient condition for high earnings**. Tour level acts as a multiplier: the same ride quality yields dramatically different prize money depending on which  our the rider competes in.

![Prize vs Score](visuals/prize_vs_score.png)

---

### 4. Tour Trends

PBR Brazil consistently shows the highest average Ride% among all tours (41-52%), while Touring Pro Division has the lowest (18-24%). Note that Ride% includes all participants. Riders with zero successful rides are counted, which reflects the real difficulty level of each tour.

UTB ride% ranges 28-38% with a growing trend since 2022, suggesting increasing competition quality at the elite level.

AVG scores show a clear hierarchy:
- **UTB**: 54-72 (elite level)
- **PBR Brazil**: 50-63
- **PBR Canada**: 43-59
- **Challenger Series**: 38-42 *(launched 2022)*
- **Touring Pro Division**: 25-32 (entry level)

![Tour Trends](visuals/tour_trends.png)

---

### 5. Rider Stability
To measure stability, I calculated the **Coefficient of Variation (CV)** of each rider's ride% across seasons:

**Method:**
1. Calculate average ride% per rider per year
2. Compute STDDEV and AVG of those yearly values
3. CV = STDDEV / AVG × 100 - lower CV means more consistent year-to-year performance
4. Stability Score = 100 - CV (easier to read: higher = more stable)

**Filters applied:** ≥4 seasons, avg ride% ≥20%, ≥50 total rides *(to ensure statistically meaningful results)*

**Key findings:**
- **John Crimber** - most stable active rider (CV = 2.58%, stability score = 97.05)
- No strong correlation between avg ride% and stability: a rider can have high ride% but be inconsistent year-to-year
- The top-right of the scatter plot (high avg ride% + high stability score) represents the most well-rounded elite performers

![Stability](visuals/stability.png)

---

## 💡 Conclusions
1. **Career path matters** - Touring Pro Division (56 riders) and Challenger Series (49 riders) are the main gateways to UTB
2. **Stability predicts success** - consistent performers (low CV) tend to have higher avg ride% over their career
3. **Tour level determines earnings** - UTB distributes ~$37M over 2020-2026 vs ~$3.4M in TPD; reaching a higher tour level has greater impact on prize money than individual ride quality
4. **Speed of progression** - 50% of UTB riders got there within 1 year *(based on 2020–2026 data)*

---

## Author
**Anna Lutsenko**  
[LinkedIn](https://www.linkedin.com/in/anna-lutsenko-1a3253405/) | [Tableau Public](https://public.tableau.com/app/profile/ann.lutsenko)
