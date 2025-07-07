-- GA4 Data Analysis Examples
-- Run individual queries with: dolt sql -q "SELECT ..."

-- 1. Traffic Overview - Top sources by sessions
SELECT 
    source,
    medium,
    SUM(sessions) as total_sessions,
    SUM(active_users) as total_users,
    AVG(avg_session_duration) as avg_duration,
    AVG(bounce_rate) as avg_bounce_rate
FROM sessions_data 
GROUP BY source, medium
ORDER BY total_sessions DESC;

-- 2. Daily Traffic Trends
SELECT 
    date,
    SUM(sessions) as daily_sessions,
    SUM(active_users) as daily_users,
    AVG(bounce_rate) as daily_bounce_rate
FROM sessions_data
GROUP BY date
ORDER BY date;

-- 3. Top Pages by Views
SELECT 
    page_path,
    page_title,
    SUM(page_views) as total_views,
    SUM(unique_page_views) as unique_views,
    AVG(avg_time_on_page) as avg_time
FROM pages_data
GROUP BY page_path, page_title
ORDER BY total_views DESC
LIMIT 10;

-- 4. Device Category Performance
SELECT 
    device_category,
    SUM(sessions) as sessions,
    SUM(active_users) as users,
    AVG(bounce_rate) as bounce_rate,
    COUNT(DISTINCT country) as countries
FROM sessions_data
GROUP BY device_category
ORDER BY sessions DESC;

-- 5. Top Events by Count
SELECT 
    event_name,
    SUM(event_count) as total_events,
    SUM(event_value) as total_value,
    COUNT(DISTINCT page_path) as pages_triggered
FROM events_data
GROUP BY event_name
ORDER BY total_events DESC;

-- 6. Geographic Analysis
SELECT 
    country,
    SUM(sessions) as sessions,
    SUM(active_users) as users,
    AVG(avg_session_duration) as avg_duration
FROM sessions_data
GROUP BY country
ORDER BY sessions DESC
LIMIT 15;

-- 7. Source/Medium Performance with Conversions
SELECT 
    s.source,
    s.medium,
    SUM(s.sessions) as sessions,
    SUM(s.active_users) as users,
    COALESCE(SUM(c.conversions), 0) as conversions,
    COALESCE(SUM(c.conversion_value), 0) as conversion_value,
    CASE 
        WHEN SUM(s.sessions) > 0 
        THEN ROUND((COALESCE(SUM(c.conversions), 0) * 100.0 / SUM(s.sessions)), 2)
        ELSE 0 
    END as conversion_rate
FROM sessions_data s
LEFT JOIN conversions_data c ON s.source = c.source AND s.medium = c.medium AND s.date = c.date
GROUP BY s.source, s.medium
HAVING sessions > 0
ORDER BY conversion_rate DESC, sessions DESC;

-- 8. Page Performance with Events
SELECT 
    p.page_path,
    p.page_title,
    SUM(p.page_views) as page_views,
    AVG(p.avg_time_on_page) as avg_time,
    COALESCE(SUM(e.event_count), 0) as total_events
FROM pages_data p
LEFT JOIN events_data e ON p.page_path = e.page_path AND p.date = e.date
GROUP BY p.page_path, p.page_title
ORDER BY page_views DESC;

-- 9. Weekly Traffic Patterns
SELECT 
    WEEK(date) as week_number,
    YEAR(date) as year,
    SUM(sessions) as weekly_sessions,
    SUM(active_users) as weekly_users,
    AVG(bounce_rate) as weekly_bounce_rate
FROM sessions_data
GROUP BY YEAR(date), WEEK(date)
ORDER BY year, week_number;

-- 10. Conversion Funnel Analysis
SELECT 
    'Total Sessions' as step,
    SUM(sessions) as count,
    100.0 as percentage
FROM sessions_data
UNION ALL
SELECT 
    'Page Views' as step,
    SUM(page_views) as count,
    ROUND(SUM(page_views) * 100.0 / (SELECT SUM(sessions) FROM sessions_data), 2) as percentage
FROM pages_data
UNION ALL
SELECT 
    'Events' as step,
    SUM(event_count) as count,
    ROUND(SUM(event_count) * 100.0 / (SELECT SUM(sessions) FROM sessions_data), 2) as percentage
FROM events_data
UNION ALL
SELECT 
    'Conversions' as step,
    SUM(conversions) as count,
    ROUND(SUM(conversions) * 100.0 / (SELECT SUM(sessions) FROM sessions_data), 2) as percentage
FROM conversions_data;

-- 11. Data Quality Check
SELECT 
    'sessions_data' as table_name,
    COUNT(*) as row_count,
    COUNT(DISTINCT date) as date_range,
    MIN(date) as start_date,
    MAX(date) as end_date
FROM sessions_data
UNION ALL
SELECT 
    'pages_data' as table_name,
    COUNT(*) as row_count,
    COUNT(DISTINCT date) as date_range,
    MIN(date) as start_date,
    MAX(date) as end_date
FROM pages_data
UNION ALL
SELECT 
    'events_data' as table_name,
    COUNT(*) as row_count,
    COUNT(DISTINCT date) as date_range,
    MIN(date) as start_date,
    MAX(date) as end_date
FROM events_data
UNION ALL
SELECT 
    'conversions_data' as table_name,
    COUNT(*) as row_count,
    COUNT(DISTINCT date) as date_range,
    MIN(date) as start_date,
    MAX(date) as end_date
FROM conversions_data;