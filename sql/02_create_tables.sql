
CREATE TABLE books (
    book_id SERIAL PRIMARY KEY,
    book_name TEXT,
    category TEXT,
    price_excl_tax NUMERIC(10,2),
    price_incl_tax NUMERIC(10,2),
    tax NUMERIC(10,2),
    availability TEXT,
    stock_count INTEGER,
    rating INTEGER,
    upc VARCHAR(50) UNIQUE,
    product_url TEXT,
    image_url TEXT,
    description TEXT,
    page_number INTEGER,
    scraped_at TIMESTAMP
);
