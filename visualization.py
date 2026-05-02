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
plt.savefig('visuals/tour_trendsz .png', dpi=150, bbox_inches='tight')
plt.show()