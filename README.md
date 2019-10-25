# Dash-App-For-Visualization
I will be uploading some interesting apps developed using Dash in python.
For now, I have only provided a network visualization of the dataset.
About Dataset:

A network of technology tags from Developer Stories on the Stack Overflow online developer community website.

This is organized as two tables:

stack_network_links contains links of the network, the source and target tech tags plus the value of the the link between each pair stack_network_nodes contains nodes of the network, the name of each node, which group that node belongs to (calculated via a cluster walktrap), and a node size based on how often that technology tag is used


Requirements:
                  
                     python: 3.7
                     plotly: 4.2.1 
                     dash: 1.4.1 
                     networkx: 2.4 
                     pandas:
                     numpy:


To run it:  
  1)First Start server using following command:
               
               >> python3 dash_networkplot.py
               
  2)After that click on the output server link from the previous command and that will open app in your default browser.
