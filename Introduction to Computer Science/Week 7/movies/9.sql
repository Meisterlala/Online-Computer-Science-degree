SELECT 
    name
FROM
    movies 
        JOIN stars on movies.id = stars.movie_id
        JOIN people on people.id = stars.person_id 
WHERE 
    year = 2004
ORDER BY 
    birth ASC;