set -eu

mysql --protocol=socket --socket=/var/run/mysqld/mysqld.sock -uroot -p"${MYSQL_ROOT_PASSWORD}" -D "${MYSQL_DATABASE}" <<'SQL'
DELETE FROM utilisateurs;

INSERT INTO utilisateurs (nom, email, mot_de_passe)
VALUES
  ('thibaud', 'thibaud@ynov.com', 'thibaud123'),
  ('gabin', 'gabin@ynov.com', 'gabin123'),
  ('arthur', 'arthur@ynov.com', 'arthur123'),
  ('killian', 'killian@ynov.com', 'killian123');
SQL
