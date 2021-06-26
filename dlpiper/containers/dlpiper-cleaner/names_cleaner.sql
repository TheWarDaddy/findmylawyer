DELETE  FROM
    names a
        USING names b
WHERE
    a.profile_id > b.profile_id
    AND a.name = b.name;

SELECT name, COUNT(name) FROM names GROUP BY name HAVING COUNT (name) > 1;
