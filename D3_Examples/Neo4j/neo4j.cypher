MATCH (movie:Movie {title:{title}})
 OPTIONAL MATCH (movie)<-[r]-(person:Person)
 RETURN movie.title as title,
       collect({name:person.name,
                job:head(split(lower(type(r)),'_')),
                role:r.roles}) as cast LIMIT 1

:POST /db/data/transaction/commit
  {"statements":[{"statement":"MATCH path = (n)-[r]->(m) RETURN path",
                  "resultDataContents":["graph"]}]}