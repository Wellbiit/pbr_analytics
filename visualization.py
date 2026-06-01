import matplotlib.pyplot as plt
import pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine('postgresql://postgres:avataranaconda2011@localhost:5432/pbr_analytics')

#Топ 10 райдерів (2020-2026) за очками
with engine.connect() as conn:
    df_top10 = pd.read_sql(text("""SELECT 
        rider
        , ROUND(SUM(points)::numeric, 2) as Points
        , SUM("prize_$") as Prize_in_USD
        , ROUND(AVG(avg_score)::numeric, 2) as Average_score
        , ROUND(AVG("ride_%")::numeric, 2) as Average_ride
        , SUM(outs) as Outs
        , SUM(rides) as Rides
        , COUNT(DISTINCT year) as Years
        , COUNT(DISTINCT tour) as Tours
    FROM riders
    GROUP BY rider
    ORDER BY 2 DESC
    LIMIT 10;"""), conn)

print(df_top10)

colors = ['#D4A017'] + ['#990000'] * 9
plt.style.use('dark_background')
plt.figure(figsize=(10, 6))
plt.barh(df_top10['rider'], df_top10['points'], color=colors)
plt.title('Top 10 PBR Riders by Total Points (2020-2026)')
plt.xlabel('Total Points')
plt.ylabel('Rider')
plt.tight_layout()
plt.savefig('visuals/top10_riders.png', dpi=150, bbox_inches='tight')
plt.show()


#Топ-5 райдерів по роках
with engine.connect() as conn:
    df_top5 = pd.read_sql(text("""
    SELECT
	    rider
	    , year
	    , ROUND(SUM(points)::numeric, 2) AS Points_per_year
	    , ROUND(SUM("prize_$")::numeric, 2) AS Prize_per_year
	    , ROUND(AVG(avg_score)::numeric, 2) AS AVG_score_per_year
	    , ROUND(AVG("ride_%")::numeric, 2) AS AVG_ride_per_year
    FROM riders
    WHERE rider IN ('Brady Fielder', 'Nick Tetz', 'Dakota Buttar', 'Dener Barbosa', 'Cody Coverchuk') 
    GROUP BY year, rider
    ORDER BY rider ASC, year ASC;"""), conn)

print(df_top5)

colors = ['#D4A017', '#990000', '#FFFFFF', '#1E90FF', '#228B22']
plt.style.use('dark_background')
plt.figure(figsize=(10, 6))

for i, rider in enumerate(df_top5['rider'].unique()):
    data = df_top5[df_top5['rider'] == rider]
    plt.plot(data['year'], data['points_per_year'], label=rider, color=colors[i],linewidth=2)

plt.legend()
plt.title('Top 5 PBR Riders: Points per year (2020-2026)')
plt.xlabel('Year')
plt.ylabel('Points')
plt.savefig('visuals/top5_riders.png', dpi=150, bbox_inches='tight')
plt.show()


#Порівняння турів за середнім Ride %
with engine.connect() as conn:
    df_tours = pd.read_sql(text("""
    SELECT 
	    tour
	    , COUNT(DISTINCT rider) AS Riders_count
	    , ROUND((SUM(rides)::numeric / NULLIF(SUM(outs), 0)) * 100, 2) AS ride_pct
	    , ROUND(AVG(avg_score)::numeric, 2) AS AVG_score_in_tour
	    , ROUND(SUM("prize_$")::numeric, 2) AS Prize_in_tour
    FROM riders
    GROUP BY tour;"""), conn)

print(df_tours)

colors = ['#990000'] * 6 + ['#D4A017']
plt.style.use('dark_background')
plt.figure(figsize=(10, 6))
plt.barh(df_tours['tour'], df_tours['ride_pct'], color=colors)
plt.title('PBR Tours: Average Ride % comparison')
plt.xlabel('Ride %')
plt.ylabel('Tour')
plt.tight_layout()
plt.savefig('visuals/tour_avg_ride%.png', dpi=150, bbox_inches='tight')
plt.show()


#Prize vs Score
with engine.connect() as conn:
    df_scatter = pd.read_sql(text("""
    SELECT 
        rider
        , ROUND(SUM(points)::numeric, 2) as Points
        , SUM("prize_$") as Prize_in_USD
        , ROUND(AVG(avg_score)::numeric, 2) as Average_score
        , ROUND(AVG("ride_%")::numeric, 2) as Average_ride
        , SUM(outs) as Outs
        , SUM(rides) as Rides
        , COUNT(DISTINCT year) as Years
        , COUNT(DISTINCT tour) as Tours
    FROM riders
    GROUP BY rider
    ORDER BY 2 DESC;"""), conn)

print(df_tours)

colors = ['#990000']
plt.style.use('dark_background')
plt.figure(figsize=(10, 6))
plt.scatter(df_scatter['average_score'], df_scatter['prize_in_usd'], color=colors)
plt.title('Prize vs Average Score per Rider (2020-2026)')
plt.xlabel('Average score')
plt.ylabel('Prize (millions)')
plt.tight_layout()
plt.savefig('visuals/prize_vs_score.png', dpi=150, bbox_inches='tight')
plt.show()


#Тренди турнірів
with engine.connect() as conn:
    df_tour_trends = pd.read_sql(text("""
    SELECT 
	    tour
	    , year
	    , COUNT(DISTINCT rider) AS Riders_count
	    , ROUND((SUM(rides)::numeric / NULLIF(SUM(outs), 0)) * 100, 2) AS ride_pct	
	    , ROUND(AVG(avg_score)::numeric, 2) AS AVG_score_in_tour
	    , ROUND(SUM("prize_$")::numeric, 2) AS Prize_in_tour
    FROM riders
    GROUP BY tour, year"""), conn)

print(df_tours)

colors = ['#990000']
plt.style.use('dark_background')
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

#Ride% по роках
for tour in df_tour_trends['tour'].unique():
    data = df_tour_trends[df_tour_trends['tour'] == tour]
    ax1.plot(data['year'], data['ride_pct'], label=tour)

ax1.set_title('Ride % by Tour per Year')
ax1.set_xlabel('Year')
ax1.set_ylabel('Ride %')
ax1.legend()

# Avg_score по роках
for tour in df_tour_trends['tour'].unique():
    data = df_tour_trends[df_tour_trends['tour'] == tour]
    ax2.plot(data['year'], data['avg_score_in_tour'], label=tour)

ax2.set_title('AVG score by Tour per Year')
ax2.set_xlabel('Year')
ax2.set_ylabel('AVG score')
ax2.legend()

plt.tight_layout()
plt.savefig('visuals/tour_trends.png', dpi=150, bbox_inches='tight')
plt.show()


#Трамплін до UTB
with engine.connect() as conn:
    df_springboard = pd.read_sql(text("""
    WITH first_year_in_PBR AS(
        SELECT rider, MIN(year) as first_year_in_PBR
        FROM riders
        GROUP BY rider
    ),
    first_year_in_UTB AS(
        SELECT rider, MIN(year) as first_year_in_UTB
        FROM riders
        WHERE tour = 'unleash_the_best'
        GROUP BY rider
    )
    SELECT
        years_to_UTB
        , COUNT(rider) as rider_count
    FROM (
        SELECT
            first_year_in_UTB.rider
            , first_year_in_UTB.first_year_in_UTB - first_year_in_PBR.first_year_in_PBR as years_to_UTB
        FROM first_year_in_UTB
        LEFT JOIN first_year_in_PBR ON first_year_in_UTB.rider = first_year_in_PBR.rider
        WHERE first_year_in_UTB.first_year_in_UTB - first_year_in_PBR.first_year_in_PBR > 0
    ) as subquery
    GROUP BY years_to_UTB
    ORDER BY years_to_UTB ASC
    """), conn)

df_springboard.to_csv('data/years_to_utb.csv', index=False, sep=';')
print(df_springboard)

colors = ['#990000']
plt.style.use('dark_background')
plt.figure(figsize=(10, 6))
plt.bar(df_springboard['years_to_utb'], df_springboard['rider_count'], color=colors)
plt.title('Springboard to UTB')
plt.xlabel('Years to UTB')
plt.ylabel('Rider count')
plt.tight_layout()
plt.savefig('visuals/years_to_utb.png', dpi=150, bbox_inches='tight')
plt.show()


#Трамплін до UTB (з якого турніру приходять)
with engine.connect() as conn:
    df_tour_springboard = pd.read_sql(text("""
    WITH first_year_UTB AS(
    SELECT 
        rider
        , MIN(year) as first_utb_year
    FROM riders
    WHERE tour = 'unleash_the_best'
    GROUP BY rider
),
debutants AS (
	SELECT rider
		, first_utb_year
	FROM first_year_utb
	WHERE first_utb_year > 2020
),
last_tour_before_utb AS(
	SELECT 
		r.rider
		, r.tour
		, r.year
		, d.first_utb_year
		, ROW_NUMBER() OVER (PARTITION BY r.rider ORDER BY r.year DESC) AS rn
	FROM riders r
	LEFT JOIN debutants d ON r.rider = d.rider
	WHERE r.tour != 'unleash_the_best' 
		AND r.year < d.first_utb_year
)
SELECT 
	tour
	, COUNT(DISTINCT rider) AS rider_count
FROM last_tour_before_utb
WHERE rn = 1
GROUP BY tour
ORDER BY rider_count
    """), conn)

tour_labels = {
    'challenger_series': 'Challenger Series',
    'touring_pro_division': 'Touring Pro Division',
    'pendleton_whisky_velocity_tour': 'Pendleton Velocity Tour',
    'pbr_brazil': 'PBR Brazil',
    'pbr_canada': 'PBR Canada',
    'pbr_australia': 'PBR Australia'
}

df_tour_springboard['tour'] = df_tour_springboard['tour'].map(tour_labels)
df_tour_springboard.to_csv('data/tour_springboard.csv', index=False)
print(df_tour_springboard)

plt.style.use('dark_background')
plt.figure(figsize=(10, 6))
colors = ['#D4A017' if t == df_tour_springboard['tour'].iloc[-1] else '#990000' for t in df_tour_springboard['tour']]
plt.barh(df_tour_springboard['tour'], df_tour_springboard['rider_count'], color=colors)
plt.title('Where UTB Riders Come From')
plt.xlabel('Number of Riders')
plt.ylabel('Tour')
plt.tight_layout()
plt.savefig('visuals/tour_springboard.png', dpi=150, bbox_inches='tight')
plt.show()



#Стабільність райдера по ride%
with engine.connect() as conn:
    df_stability = pd.read_sql(text("""
WITH yearly_stat AS (
    SELECT 
        rider
        , year
        , AVG("ride_%") as avg_ride_year
        , AVG(avg_score) as avg_score_year
        , SUM(rides) as total_rides_year
        , SUM(outs) as total_outs_year
    FROM riders
    GROUP BY rider, year
)
SELECT
    rider
    , ROUND(STDDEV(avg_ride_year)::numeric, 2) as st_dev_ride
    , ROUND(AVG(avg_ride_year)::numeric, 2) as avg_ride
    , ROUND(STDDEV(avg_score_year)::numeric, 2) as st_dev_score
    , ROUND(AVG(avg_score_year)::numeric, 2) as avg_score
    , ROUND((STDDEV(avg_ride_year) / NULLIF(AVG(avg_ride_year), 0) * 100)::numeric, 2) as cv_ride
    , ROUND((100 - (STDDEV(avg_ride_year) / NULLIF(AVG(avg_ride_year), 0) * 100))::numeric, 2) as stability_score
    , COUNT(DISTINCT year) as year_count
    , SUM(total_rides_year) as total_rides
    , SUM(total_outs_year) as total_outs
FROM yearly_stat
GROUP BY rider
HAVING COUNT(year) >= 4
    AND AVG(avg_ride_year) >= 20
    AND SUM(total_rides_year) >= 50
ORDER BY cv_ride ASC
    """), conn)

print(df_stability)

colors = ['#990000']
plt.style.use('dark_background')
plt.figure(figsize=(10, 6))
plt.scatter(df_stability['avg_ride'], df_stability['stability_score'], color=colors)
top5 = df_stability.nlargest(5, 'stability_score')
for _, row in top5.iterrows():
    plt.annotate(row['rider'], (row['avg_ride'], row['stability_score']),
                textcoords="offset points", xytext=(5, 5),
                fontsize=8, color='#D4A017')
plt.title('Rider stability')
plt.xlabel('Average ride %')
plt.ylabel('Stability score')
plt.tight_layout()
plt.savefig('visuals/stability.png', dpi=150, bbox_inches='tight')
plt.show()
df_stability.to_csv('data/stability.csv', index=False)
print('stability.csv exported')

#Експорт даних для Tableau
with engine.connect() as conn:
    df_tableau = pd.read_sql(text("SELECT * FROM riders"), conn)
    df_tableau.columns = ['num', 'rider', 'points', 'avg_score', 'prize', 'outs', 'rides', 'ride_pct', 'tour', 'year']
    df_tableau.to_csv('data/riders_for_tableau.csv', index=False)
    print('Tableau CSV exported!')