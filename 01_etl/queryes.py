# Вернеет данные, которые следует обновить
FW_SQL = """
SELECT fw.id,
       fw.title,
       fw.description,
       fw.rating,
       fw.type,
       fw.created,
       fw.modified,
       COALESCE(
           JSON_AGG(
               DISTINCT JSONB_BUILD_OBJECT(
                   'person_id', p.id,
                   'person_name', p.full_name
                   )
               ) FILTER (WHERE p.id IS NOT NULL and pfw.role = 'actor'),
           '[]'
           ) AS actors,
       COALESCE(
           JSON_AGG(
               DISTINCT JSONB_BUILD_OBJECT(
                   'person_id', p.id,
                   'person_name', p.full_name
                   )
               ) FILTER (WHERE p.id IS NOT NULL and pfw.role = 'writer'),
           '[]'
           ) AS writers,
        ARRAY_AGG(DISTINCT p.full_name)
            FILTER(WHERE pfw.role = 'director') AS director,
        ARRAY_AGG(DISTINCT p.full_name)
            FILTER(WHERE pfw.role = 'writer') AS writers_names,
        ARRAY_AGG(DISTINCT p.full_name)
            FILTER(WHERE pfw.role = 'actor') AS actors_names,
       ARRAY_AGG(DISTINCT g.name) AS genres
FROM content.film_work fw
         LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
         LEFT JOIN content.genre g ON g.id = gfw.genre_id
         LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
         LEFT JOIN content.person p ON p.id = pfw.person_id
WHERE
    fw.modified > '{date_time}'
OR
    fw.id in (
        SELECT pfw.film_work_id
        FROM person p
            INNER JOIN person_film_work pfw ON p.id = pfw.person_id
        WHERE p.modified > '{date_time}'
        )
OR
    fw.id in (
        SELECT gfw.film_work_id
        FROM genre g
            INNER JOIN genre_film_work gfw ON g.id = gfw.genre_id
        WHERE g.modified > '{date_time}'
        )
GROUP BY fw.id
ORDER BY fw.modified;
"""

# Вернет все данные
ALL_DATA_SQL = """
SELECT fw.id,
       fw.title,
       fw.description,
       fw.rating,
       fw.type,
       fw.created,
       fw.modified,
       COALESCE(
           JSON_AGG(
               DISTINCT JSONB_BUILD_OBJECT(
                   'person_id', p.id,
                   'person_name', p.full_name
                   )
               ) FILTER (WHERE p.id IS NOT NULL and pfw.role = 'actor'),
           '[]'
           ) AS actors,
       COALESCE(
           JSON_AGG(
               DISTINCT JSONB_BUILD_OBJECT(
                   'person_id', p.id,
                   'person_name', p.full_name
                   )
               ) FILTER (WHERE p.id IS NOT NULL and pfw.role = 'writer'),
           '[]'
           ) AS writers,
        ARRAY_AGG(DISTINCT p.full_name)
            FILTER(WHERE pfw.role = 'director') AS director,
        ARRAY_AGG(DISTINCT p.full_name)
            FILTER(WHERE pfw.role = 'writer') AS writers_names,
        ARRAY_AGG(DISTINCT p.full_name)
            FILTER(WHERE pfw.role = 'actor') AS actors_names,
       ARRAY_AGG(DISTINCT g.name) AS genres
FROM content.film_work fw
         LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
         LEFT JOIN content.genre g ON g.id = gfw.genre_id
         LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
         LEFT JOIN content.person p ON p.id = pfw.person_id
GROUP BY fw.id
ORDER BY fw.modified;
"""
