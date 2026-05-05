# Public sector pay across 13 large U.S. cities

Apples-to-apples side-by-side comparison of contract base salary for police officers,
firefighters, sanitation workers and transit bus operators across 13 large U.S. cities,
drawn directly from collective bargaining agreements, official city pay schedules and
department careers pages.

**Live site:** https://joshgreenman1973.github.io/public-sector-pay/

## Three views

- **By role** — sortable table of one role across all 13 cities, with averages and a ranked bar chart.
- **By city** — full pay profile for one city across all 4 roles.
- **NYC focus** — NYC's rank, percentile and dollar gap vs. each peer city for every role and metric, with toggles for cost-of-living adjustment (BEA Regional Price Parities, 2023) and NYC "all-in" top-step (base + longevity + holiday + uniform + differentials).

## Data

- 13 cities: New York, Los Angeles, Chicago, Houston, Phoenix, Philadelphia, San Antonio, San Diego, Dallas, San Francisco, Boston, Seattle, Washington D.C.
- 4 roles per city = 52 cells, each cell either populated from a sourced contract / pay schedule or marked "private contractor" or "data gap" with explanation.
- Every figure links to the source document.

## Sources

All from official city or transit-authority pages: city Office of Labor Relations, city
Comptroller / HR salary schedules, transit-authority CBAs, department careers pages.
No third-party aggregators (no Glassdoor, Indeed, Transparent California). The
methodology page in the site enumerates every URL by city.

Cost-of-living index: U.S. Bureau of Economic Analysis, Regional Price Parities by
Metropolitan Statistical Area (MARPP), 2023.

## Caveats

This is **base salary only**. Officers and firefighters earn meaningfully more in total
take-home pay due to overtime, longevity, holiday, uniform, education and detail pay.
The NYC "all-in" toggle in the NYC focus tab approximates total comp at top step
(excluding overtime).

## Run locally

```
cd site && python3 -m http.server 8000
```

Then open http://localhost:8000.
