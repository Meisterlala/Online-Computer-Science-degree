SELECT 
    name
FROM
    movies 
        JOIN directors on movies.id = directors.movie_id
        JOIN people on people.id = directors.person_id 
        Join ratings on ratings.movie_id = directors.movie_id
WHERE 
    rating >= 9.0
ORDER BY 
    birth ASC;