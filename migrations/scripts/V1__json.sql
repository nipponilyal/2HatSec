CREATE table txtmessage (
    mcount INT,
    mtext VARCHAR(10000), 
    player VARCHAR(20), 
    flags INT,
    client_id INT,
    filtered INT,
    simplified VARCHAR(10000)
);

CREATE table topics (
    client_id INT, 
    simplified VARCHAR(10000),
    topic INT,
    confidence INT,
    relevance INT
);
