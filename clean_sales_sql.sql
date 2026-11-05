CREATE OR REPLACE VIEW clean_sales AS
SELECT DISTINCT 
    order_id,
    TRIM(UPPER(REPLACE(city, '"', ''))) AS city_clean,
    COALESCE(amount, 0) AS amount_clean,
    load_date
FROM raw_sales;