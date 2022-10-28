library(igraph)
library (qgraph)
library(zoom)

# Read in data and create variables
G=read.graph("st_graph.gml","gml")
e <- get.edgelist(G)
l <- qgraph.layout.fruchtermanreingold(e,vcount=vcount(G),area=9*(vcount(G)^2),repulse.rad=(vcount(G)^3.1))
PageWeights=max(E(G)$weight+1)-E(G)$weight #pagerank uses affinity rather than distance weights on edges
clusters <- cluster_walktrap(G)$membership 

# Community statistics
modularity(wc)
membership(wc)

colbar <- rainbow(max(clusters)+1)
V(G)$color <- colbar[clusters+1]
V(G)[V(G)$repo==1]$shape <- "square"
V(G)[V(G)$repo==0]$shape <- "circle"

# Large Graph Plot
plot(G, 
     vertex.frame.color = "black", # set vertex border color
     vertex.label = NA,
     edge.arrow.mode=0,
     edge.width=.01,
     vertex.size=(page.rank(G)$vector+0.012)/max(page.rank(G)$vector)*7.5,
     edge.color = "black", # set edge color
     layout=l
)


# Small graph plot
V(G)[V(G)$repo==1]$shape <- "square"
V(G)[V(G)$repo==1]$color <- "cyan"
V(G)[V(G)$repo==1]$size <- 10
V(G)[V(G)$repo==0]$shape <- "circle"
V(G)[V(G)$repo==0]$color <- "purple"
V(G)[V(G)$repo==1]$size <- 5

plot(G,
     vertex.frame.color = "black", # set vertex border color
     edge.arrow.size=.2,
     edge.color = "black", # set edge color
     layout=l
)