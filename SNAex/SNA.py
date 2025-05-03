#####################################################################
####### Peer-to-Peer Mobile Lending in a Digital Finance App ########
#####################################################################
"""
A fintech company runs a mobile app that lets users send money to friends, borrow small amounts, and 
repay loans without traditional banks. You're analyzing user interactions over 3 months to understand 
how influence and trust spread in the network.
"""
####### Simplified interaction types: #######
"""
We are goint to work in a directed network, with arc (->) showing the direction, for intance:

A -> B: A sent money to B

B -> A: B repaid a loan from A

C -> A: C borrowed from A

From these interactions, a directed network is created where nodes are users and edges represent money flow.
Thereafter, from the directed network, key Social Network Analysis metrics are calculated to understand 
the network structure and identify key users.
"""

####### Social Network Analysis (SNA) #######

"""
Social Network Analysis studies relationships and interactions among entities (called nodes) through the connections (edges) that link them.
Moreover, the metrics used to perform this analysis in graphs transform structure into meaning. 
They help identify the roles of entities in the network, as well as risks, opportunities, and strategies within complex social or such, 
in this case, financial systems. 

The metrics help to answer questions such as:
 - Who are the most trusted users who receive money frequently?
 - If a key user is removed, which other users would lose connectivity?
 - Who could spread a new feature or incentive fastest (e.g., referral program)? 
"""
###########################
######## Libraries ########
###########################
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

###########################################
######## Create a Directed Network ########
###########################################

# Creates a directed netork
G= nx.DiGraph() 

# Create the nodes of the network
# Showing interactions between different nodes (users)
edges = [
    ("Alice", "Bob"),    # Alice sent money to Bob
    ("Alice", "Eve"),    # Alice sent money to Eve
    ("Alice", "Charlie"),# Alice sent money to Charlie
    ("Alice", "Dana"),   # Alice sent money to Dana
    ("Bob", "Alice"),    # Bob repaid Alice
    ("Bob", "Charlie"),  # Bob sent money to Charlie
    ("Bob", "Eve"),      # Bob sent money to Eve
    ("Charlie", "Alice"),# Charlie repaid Alice     
    ("Charlie", "Eve"),  # Charlie sent money to Eve
    ("Charlie", "Dana"), # Charlie sent money to Eve
    ("Dana", "Eve"),     # Dana sent money to Eve
    ("Eve", "Alice"),    # Eve repaid Alice 
]

# Add the edges to the graph 
G.add_edges_from(edges)

#######################################################
######## Visualization of the Directed Network ########
#######################################################
"""
The following code creates a directed network representing money transactions between users. 
"""

# Set the figure size and create a new figure
plt.figure(num="Transaction Network Visualization", figsize=(12, 8))

# Define fixed positions for visual layout
pos = {
    "Alice": (0, 1),
    "Bob": (3, 0),
    "Charlie": (2, 1),
    "Eve": (1, -0.5),
    "Dana": (-1, 0),
}

# Draw edges with margins so arrows "stop" at node borders
nx.draw_networkx_edges(
    G,
    pos=pos,
    arrowstyle='-|>',
    arrowsize=45,
    edge_color='black',
    width=2,
    connectionstyle='arc3,rad=0.1',
    min_source_margin=25,
    min_target_margin=25
)

# Draw nodes
nx.draw_networkx_nodes(
    G, pos=pos, node_color="purple", node_size=4000, alpha=1
)
# Set node labels
nx.draw_networkx_labels(
    G, pos=pos, font_size=14, font_color='white', font_weight='bold'
)

# Set the figure title and remove axis
plt.title("Network of Transactions Between Users", fontsize=18, fontweight='bold', color='black')
plt.axis('off')

# Automatically adjust the layout to fit the figure
plt.tight_layout()

# Save the figure as a PNG file in the current directory
plt.savefig("network_visualization.png", format="png", dpi=300)

# Show the plot
plt.show()

#########################
######## Metrics ########
#########################

######## Degree Centrality ########
"""
This metric use number of connections a node has (in and out separately for directed networks) to identify 
active participants (many transactions) or highly requested users.

The Degree Centrality metric provides information that allows us to answer these questions:
 
Q1: Who is the most active user sending money (high out-degree)?
 
Q2: Who is the most trusted user receiving money frequently (high in-degree)?

Note:
    - High out-degree = lender or sender.

    - high in-degree = popular receiver or target of transactions.
"""

######## Get in-degree and out-degree centrality ########
 
# In-Degree: Number of incoming edges (money received)
in_deg = dict(G.in_degree()) # {user: in-degree value}

# Out-Degree: Number of outgoing edges (money sent)
out_deg = dict(G.out_degree()) # {user: out-degree value}

# Highest in-degree
max_in_deg_user = max(in_deg, key=in_deg.get)
max_in_deg_value = in_deg[max_in_deg_user]

# Highest out-degree
max_out_deg_user = max(out_deg, key=out_deg.get)
max_out_deg_value = out_deg[max_out_deg_user]

# Print the answers to the questions Q1 and Q2:
print(f"The most active user receiving money frequently: {max_in_deg_user} ({max_in_deg_value})")
print(f"The most trusted user sending money: {max_out_deg_user} ({max_out_deg_value})")


######## Creates a bar plot to visualize in-degree and out-degree centrality for each user ########

# Get the users list and their in-degree and out-degree values
users = list(G.nodes())
in_values = [in_deg[user] for user in users]
out_values = [out_deg[user] for user in users]

# x-coordinates for the bars
x = np.arange(len(users))
width = 0.35 # the width of the bars

# Set the figure size and create a new figure
plt.figure(num="Degree Centrality", figsize=(8, 6))

# Set the bar width for In-Degree and Out-Degree
plt.bar(x - width/2, in_values, width, label='In-Degree', color='#1fde52') 
plt.bar(x + width/2, out_values, width, label='Out-Degree', color='red')

# Set the x-ticks and labels
plt.xticks(x, users)
plt.xlabel('Users', fontsize=14)

# Set the y-ticks and labels
plt.yticks(np.arange(0, max(max(in_values), max(out_values)) + 1, 1))
plt.ylabel('Degree', fontsize=14, )

# Set the title and legend
plt.title('In-Degree and Out-Degree Centrality per User', fontsize=16, fontweight='bold')
plt.legend()

# Set# Automatically adjust the layout to fit the figure 
plt.tight_layout()

# Save the figure as a PNG file in the current directory
plt.savefig("degree_centrality.png", format="png", dpi=300)

# Show the plot
plt.show()


######## Betweenness Centrality ########
"""
The betweenness centrality measures how often a node lies on the shortest paths between two other nodes. Let's picture this with the analogy of a major airport hub—many routes go through it because that way, the route is shorter.

This metric allows us to address this question:

Q3: Who is the user that act as bridges within the community (e.g., lenders)?

Note:

High betweenness = A high betweenness for an user, in the context of financial transactions, indicates
that is financial gatekeeper with significant influence, as it connects many users and can either
delay, facilitate, or block interactions.
"""


######## Get the Betweenness Centrality of each user ########

bet_cen = nx.betweenness_centrality(G) #{user: betweenness centrality}

# Highest betweenness centrality
max_bet_user = max(bet_cen, key=bet_cen.get)
max_bet_value = bet_cen[max_bet_user]

# Print the answer to the question Q3:
print(f"The user that act as bridge within the network is {max_bet_user} ({max_bet_value:.4f})")


######## Creates a bar plot to visualize betweenness centrality for each user ########

# Betweenness centrality value of each user
bet_values = [bet_cen[user] for user in users]

# Set the figure size and create a new figure
plt.figure(num="Betweenness Centrality", figsize=(8, 6))

# Set the bar input data, width and color
plt.bar(users, bet_values, color='purple')

# Set the x-axis labels and font size
plt.xlabel('Users', fontsize=14)

# Set the y-axis labels and font size
plt.ylabel('Betweenness Centrality',fontsize=14)

# Set the title and font size
plt.title('Betweenness Centrality per User',fontsize=16, fontweight='bold')

# Set automatically adjust the layout to fit the figure
plt.tight_layout()

# Save the figure as a PNG file in the current directory
plt.savefig("betweenness_centrality.png", format="png", dpi=300)

# Show the plot
plt.show()


######## Closeness Centrality ########
"""_summary_
It measures how close, on average, a node is to all other nodes in the network based on the shortest paths.
You can catch this as a person in a city center who can reach everyone faster than someone in a remote village
because, on average, that person is closest to the others.  

This metric help us to answer the question:

Q4: Who is the user in “central” positions who could be promoted to become an agent?

**Note:**
**High closeness = short average distance to every node in the network**
"""

# Get the Closeness Centrality of each user as a dictionary: {user: closeness centrality}
clo_cen = nx.closeness_centrality(G)

# User with highest closeness centrality
max_clo_user = max(clo_cen, key=clo_cen.get)
max_clo_value = clo_cen[max_clo_user]

print(f"The user that could be promoted to become an agent is: {max_clo_user} ({max_clo_value:.2f})")


######## Creates a bar plot to visualize closeness centrality for each user ########

# Closeness centrality value list of each user in the network
clo_values = [clo_cen[user] for user in users]

# Set the figure size and create a new figure
plt.figure(num="Closeness Centrality", figsize=(8, 6))

# Set the bar input data, width and color
plt.bar(users, clo_values, color='purple')

# Set the x-axis labels and font size
plt.xlabel('Users', fontsize=14)

# Set the y-axis labels and font size
plt.ylabel('Closeness Centrality', fontsize=14) 

# Set title and font size
plt.title('Closeness Centrality per User', fontsize=16, fontweight='bold')         

# Set automatically adjust the layout to fit the figure
plt.tight_layout()

# Save the figure as a PNG file in the current directory
plt.savefig("Closeness_Centrality.png", format="png", dpi=300)

# Show the plot
plt.show()


######## Average Distance: Closeness Centrality variation ########

"""
The average distance of a node to all other nodes in the network can be calculated as the inverse of its Closeness Centrality:
                                      Inverse Closeness Centrality = 1 / Closeness Centrality(Node)

This represents the average number of steps required to reach any other node in the network from the given node.

This variation of the metric helps answer the question:

Q5: On average, how many connections (or steps) away is the “central” individual from others in the network?
"""

# Get the average number of connections to reach any other user from the user with the highest closeness centrality
inverse_clo_cen_values=1/ clo_cen[max_clo_user]

# Print the answer to the question Q5:
print(f"On average, {max_clo_user} needs {round(inverse_clo_cen_values,2)} connections to reach any other user within the network.")


######## Creates a bar plot to visualize inverse closeness centrality for each user ########

# The average distance for the users to reach all users in the network
# Calculate the inverse of closeness centrality for each user
inverse_clo_cen = {user: 1 / value if value > 0 else 0 for user, value in clo_cen.items()}

# Get the inverse closeness centrality values for each user
inverse_clo_cen_values = [inverse_clo_cen[user] for user in users]

# Set the figure size and create a new figure
plt.figure(num="Inverse Closeness Centrality", figsize=(8, 6))

# Set the bar input data, width and color
plt.bar(users, inverse_clo_cen_values, color='purple')

# Set the x-axis label and font size
plt.xlabel('Users', fontsize=14)

# Set the y-axis label and font size
plt.ylabel('Inverse Closeness Centrality', fontsize=14)

# Set the title and font size
plt.title('Inverse Closeness Centrality per User', fontsize=16, fontweight='bold')         

# Set automatically adjust the layout to fit the figure
plt.tight_layout()

# Save the figure as a PNG file in the current directory
plt.savefig("inverse_closeness_centrality.png", format="png", dpi=300)

# Show the plot
plt.show()

