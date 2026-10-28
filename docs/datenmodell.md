## Ist-Zustand

### Bets

| table_name | column_name | data_type | is_nullable | Hinweis |
| ---------- | ----------- | --------- | ----------- | ------- |
| bets       | id          | text      | NO          |         |
| bets       | amount      | real      | YES         |         |
| bets       | odds        | real      | YES         |         |
| bets       | prediction  | text      | YES         |         |
| bets       | match_id    | bigint    | YES         |         |
| bets       | status      | text      | YES         |         |

### Matches

| table_name | column_name     | data_type | is_nullable | Hinweis |
| ---------- | --------------- | --------- | ----------- | ------- |
| matches    | fixture_id      | bigint    | NO          |         |
| matches    | fixture_date    | text      | NO          |         |
| matches    | fixture_status  | text      | YES         |         |
| matches    | league_id       | bigint    | YES         |         |
| matches    | league_name     | text      | YES         |         |
| matches    | league_round    | text      | YES         |         |
| matches    | teamhome_name   | text      | YES         |         |
| matches    | teamhome_logo   | text      | YES         |         |
| matches    | teamhome_winner | boolean   | YES         |         |
| matches    | teamaway_name   | text      | YES         |         |
| matches    | teamaway_logo   | text      | YES         |         |
| matches    | teamaway_winner | boolean   | YES         |         |
| matches    | goal_home       | bigint    | YES         |         |
| matches    | goal_away       | bigint    | YES         |         |
| matches    | odd_home        | real      | YES         |         |
| matches    | odd_draw        | real      | YES         |         |
| matches    | odd_away        | real      | YES         |         |

### User

| table_name | column_name | data_type | is_nullable | Hinweis |
| ---------- | ----------- | --------- | ----------- | ------- |
| users      | id          | bigint    | NO          |         |
| users      | username    | text      | NO          |         |
| users      | balance     | real      | YES         |         |
| users      | user_id     | text      | YES         |         |

### System Value

| table_name    | column_name | data_type | is_nullable | Hinweis |
| ------------- | ----------- | --------- | ----------- | ------- |
| system_values | key         | text      | NO          |         |
| system_values | value       | text      | NO          |         |

## Soll-Zustand

### Bets

| table_name | column_name | data_type   | is_nullable | Hinweis                               |
| ---------- | ----------- | ----------- | ----------- | ------------------------------------- |
| bets       | id          | bigint      | NO          | Primärschlüssel                       |
| bets       | user_id     | uuid        | NO          | Fremdschlüssel auf users.id           |
| bets       | match_id    | bigint      | NO          | Fremdschlüssel auf matches.fixture_id |
| bets       | amount      | numeric     | YES         | > 0                                   |
| bets       | odds        | numeric     | YES         |                                       |
| bets       | prediction  | text        | YES         | home, draw oder away                  |
| bets       | status      | text        | YES         | open, won oder lost                   |
| bets       | created_at  | timestamptz | YES         |                                       |

### Matches

| table_name | column_name     | data_type | is_nullable | Hinweis |
| ---------- | --------------- | --------- | ----------- | ------- |
| matches    | fixture_id      | bigint    | NO          |         |
| matches    | fixture_date    | text      | NO          |         |
| matches    | fixture_status  | text      | YES         |         |
| matches    | league_id       | bigint    | YES         |         |
| matches    | league_name     | text      | YES         |         |
| matches    | league_round    | text      | YES         |         |
| matches    | teamhome_name   | text      | YES         |         |
| matches    | teamhome_logo   | text      | YES         |         |
| matches    | teamhome_winner | boolean   | YES         |         |
| matches    | teamaway_name   | text      | YES         |         |
| matches    | teamaway_logo   | text      | YES         |         |
| matches    | teamaway_winner | boolean   | YES         |         |
| matches    | goal_home       | bigint    | YES         |         |
| matches    | goal_away       | bigint    | YES         |         |
| matches    | odd_home        | real      | YES         |         |
| matches    | odd_draw        | real      | YES         |         |
| matches    | odd_away        | real      | YES         |         |

### User

| table_name | column_name | data_type   | is_nullable | Hinweis                                      |
| ---------- | ----------- | ----------- | ----------- | -------------------------------------------- |
| users      | id          | uuid        | NO          | Primärschlüssel, verweist auf auth.users(id) |
| users      | username    | text        | NO          |                                              |
| users      | balance     | numeric     | YES         | Startwert 100                                |
| users      | created_at  | timestamptz | YES         |                                              |

### System Value

| table_name    | column_name | data_type | is_nullable | Hinweis |
| ------------- | ----------- | --------- | ----------- | ------- |
| system_values | key         | text      | NO          |         |
| system_values | value       | text      | NO          |         |
