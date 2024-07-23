WITH quarterly_visits AS (
---Calculate the total number of visits each site received per quarter
    SELECT
        site,
        country,
        year,
        (CASE
            WHEN month IN (1, 2, 3) THEN 1
            WHEN month IN (4, 5, 6) THEN 2
            WHEN month IN (7, 8, 9) THEN 3
            ELSE 4
        END) AS quarter,
        SUM(visits) AS total_visits
    FROM site_monthly_visits
    GROUP BY site, country, year, quarter
),
qoq_changes AS (
---Calculate the change in visits from one quarter to the next
    SELECT
        q1.site,
        q1.country,
        q1.quarter AS prev_quarter,
        q1.total_visits AS prev_q_visits,
        q2.quarter AS next_quarter,
        q2.total_visits AS next_q_visits,
        q2.total_visits - q1.total_visits AS qoq_visits_change
    FROM
        quarterly_visits q1
    JOIN
        quarterly_visits q2
    ON
        q1.site = q2.site AND
        q1.country = q2.country AND
        q1.year = q2.year AND
        q1.quarter = q2.quarter - 1
),
top_qoq_changes AS (
---Rank the sites based on the QoQ change within each country and filter out only positive changes
    SELECT
        country,
        site,
        prev_q_visits,
        next_q_visits,
        qoq_visits_change,
        ROW_NUMBER() OVER (PARTITION BY country ORDER BY qoq_visits_change DESC) AS rank
    FROM
        qoq_changes
    WHERE
        qoq_visits_change > 0
)
SELECT
---Retrieve the final results
    tqc.country,
    cc.country_name,
    tqc.site,
    scs.category,
    tqc.prev_q_visits,
    tqc.next_q_visits,
    tqc.qoq_visits_change
FROM
    top_qoq_changes tqc
JOIN
    site_category scs ON tqc.site = scs.site
JOIN
    country_mapping cc ON tqc.country = cc.country
WHERE
    tqc.rank <= 10
ORDER BY
    tqc.country, tqc.qoq_visits_change DESC;
