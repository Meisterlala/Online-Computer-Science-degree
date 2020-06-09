SELECT 
    AVG(rating)
FROM
    movies JOIN ratings on movies.id = ratings.movie_id
WHERE 
    year=2012
ORDER BY title ASC;