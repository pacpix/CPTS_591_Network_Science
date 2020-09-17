library(igraph)
library (qgraph)
library(zoom)

# Read in data and create variables
G=read.graph("st_graph.gml","gml")
e <- get.edgelist(G)
l <- qgraph.layout.fruchtermanreingold(e,vcount=vcount(G),area=9*(vcount(G)^2),repulse.rad=(vcount(G)^3.1))
PageWeights=max(E(G)$weight+1)-E(G)$weight #pagerank uses affinity rather than distance weights on edges
wc <- cluster_walktrap(G)

# Community statistics
modularity(wc)
membership(wc)

# Graph plot with clusters
V(G)[V(G)$repo==1]$shape <- "square"
V(G)[V(G)$repo==1]$color <- "cyan"
V(G)[V(G)$repo==1]$size <- 5
V(G)[V(G)$repo==0]$shape <- "circle"
V(G)[V(G)$repo==0]$color <- "purple"
V(G)[V(G)$repo==0]$size <- 5
plot(wc,
     G,
     vertex.label = NA)
zm()


# Original graph plot
V(G)[V(G)$repo==1]$shape <- "square"
V(G)[V(G)$repo==1]$color <- "cyan"
V(G)[V(G)$repo==1]$size <- 10
V(G)[V(G)$repo==0]$shape <- "circle"
V(G)[V(G)$repo==0]$color <- "purple"
V(G)[V(G)$repo==0]$size <- 5

plot(G,
     vertex.frame.color = "black", # set vertex border color
     vertex.label = NA,
     edge.arrow.size=.1,
     edge.arrow.size=.1,
     edge.color = "black", # set edge color
     layout=l
)

zm()

