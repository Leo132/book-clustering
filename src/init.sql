CREATE DATABASE IF NOT EXISTS book_clustering;

USE book_clustering;

CREATE TABLE IF NOT EXISTS phouses (
  phouse_id    bigint unsigned NOT NULL AUTO_INCREMENT,
  phouse_name            VARCHAR(255) NOT NULL,
  total_books     INT unsigned NOT NULL,
  average_price   DECIMAL(10,2) unsigned NOT NULL,
  PRIMARY KEY (phouse_id)
);

CREATE TABLE IF NOT EXISTS authors (
  author_id       bigint unsigned NOT NULL AUTO_INCREMENT,
  author_name            VARCHAR(255) NOT NULL,
  total_books     INT unsigned NOT NULL,
  average_price   DECIMAL(10, 2) unsigned NOT NULL,
  PRIMARY KEY (author_id)
);

CREATE TABLE IF NOT EXISTS clusters (
  cluster_id      bigint unsigned NOT NULL AUTO_INCREMENT,
  book_num        INT unsigned NOT NULL,
  average_price   DECIMAL(10,2) unsigned NOT NULL,
  average_pages   DECIMAL(10,2) unsigned NOT NULL,
  average_time    DECIMAL(10,2) unsigned NOT NULL,
  PRIMARY KEY (cluster_id)
);

CREATE TABLE IF NOT EXISTS users (
  user_id         bigint unsigned NOT NULL AUTO_INCREMENT,
  name            VARCHAR(255) NOT NULL,
  username        VARCHAR(255) NOT NULL,
  password        VARCHAR(255) NOT NULL,
  PRIMARY KEY (user_id)
);

CREATE TABLE IF NOT EXISTS books (
  ISBN13          VARCHAR(13) NOT NULL,
  phouse_id       bigint unsigned NOT NULL,
  cluster_id      bigint unsigned NOT NULL,
  book_name            VARCHAR(255) NOT NULL,
  category        VARCHAR(255) NOT NULL,
  published_date  DATE NOT NULL,
  pages           INT unsigned NOT NULL,
  price           DECIMAL(10, 2) unsigned NOT NULL,
  PRIMARY KEY (ISBN13),
  FOREIGN KEY(phouse_id) REFERENCES phouses(phouse_id),
  FOREIGN KEY(cluster_id) REFERENCES clusters(cluster_id)
);

CREATE TABLE IF NOT EXISTS writing (
  author_id       bigint unsigned NOT NULL,
  ISBN13          VARCHAR(13) NOT NULL,
  FOREIGN KEY(author_id) REFERENCES authors(author_id) ON DELETE CASCADE,
  FOREIGN KEY(ISBN13) REFERENCES books(ISBN13) ON DELETE CASCADE
);

-- 收藏書單
CREATE TABLE IF NOT EXISTS collections (
  user_id         bigint unsigned NOT NULL,
  ISBN13          VARCHAR(13) NOT NULL,
  PRIMARY KEY (user_id, ISBN13),
  FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE,
  FOREIGN KEY(ISBN13) REFERENCES books(ISBN13) ON DELETE CASCADE
);