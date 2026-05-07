-- 1. На всякий случай удаляем старые таблицы, чтобы начать с чистого листа
--    (сначала удаляем "дочерние" таблицы, которые ссылаются на другие)
DROP TABLE IF EXISTS suppliers CASCADE;
DROP TABLE IF EXISTS prices CASCADE;
DROP TABLE IF EXISTS products CASCADE;

-- 2. Создаем "родительскую" таблицу products.
--    У нее есть первичный ключ id, на который мы и будем ссылаться.
CREATE TABLE products (
    id SERIAL PRIMARY KEY,          -- Это и есть тот самый столбец "id"
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50)
);

-- 3. Теперь создаем "дочернюю" таблицу prices.
--    На данный момент products и ее колонка id уже существуют.
CREATE TABLE prices (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(id), -- Ссылка на ТОЛЬКО ЧТО созданную колонку
    price NUMERIC(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);