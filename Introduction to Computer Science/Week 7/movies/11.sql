SELECT 
    title
FROM
    movies 
        JOIN stars on stars.movie_id = movies.id
        JOIN people on people.id = stars.person_id 
        Join ratings on ratings.movie_id = movies.id        
WHERE 
    name = 'Chadwick Boseman'
ORDER BY 
    rating DESC
LIMIT
    5;