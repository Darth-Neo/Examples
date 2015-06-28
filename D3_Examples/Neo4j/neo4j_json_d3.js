
var nodes=[];
var links=[];

function idIndex(a,id)
{
    for (var i=0;i<a.length;i++)
    {
        if (a[i].id == id)
            return i;
    }
    return null;
}

res.results[0].data.forEach(
    function (row)
    {
        row.graph.nodes.forEach(
            function (n)
            {
                if (idIndex(nodes,n.id) == null)
                    nodes.push({id:n.id,label:n.labels[0],title:n.properties.name});
            }
        );

        links = links.concat(
            row.graph.relationships.map(
                function(r)
                {
                    return {start:idIndex(nodes,r.startNode),end:idIndex(nodes,r.endNode),type:r.type};
                }
            )
        );
    }
);

viz = {nodes:nodes, links:links};