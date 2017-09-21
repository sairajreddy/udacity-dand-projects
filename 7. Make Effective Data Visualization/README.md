# Final Summary.
---------------------------------

* Previously, I have worked and analyzed the Titanic dataset as part of another project (Investigate a dataset) in this ND course. One of the clear findings from the work was that the female survival rate was higher than the male survival rate. 

* In this project, the viz will be detailed and interactive based on the findings from my previous project i.e Female survival rate > Male survival rate. 

* This visualisation will depict how other factors influence the survival rate, the two factors that I have considered is -- Age and Ticket price (Dollars). 


# Final Design.
--------------------------------

## Design of chosen variables : 

* The concept can be dissected to form following variables : Male Survived, Male Not Survived, Female Survived and Female not survived w.r.t Age and Ticket prices.

* Based on my favorite suggestion from feedback, I have decided to include choice-based focus of the variables. i.e, a user can focus on variables he is most interested to know about. A Multi Choice check box option is part of the UI.

## Plot design :

* The feedback influenced my plot design as well, some of them suggesting it to keep it simple whereas some of were happy with my first version which just had scatter-plot based graph.  

* Therfore, I have decided to represent the data in two ways.
	1. An interactive scatter plot which shows the scatter across the age based on ticket prices. Hovering over the scatter points should show complete info of that passenger. 
	2. Summary plot using bar graph to convey survival rate against ticket price, irrespective of age.


## Axis and legends design :

* In the scatter plot, the x-axis focuses on age whereas y-axis will be the ticket range. The legends will show the variables as discussed. Where, shapes represent the gender (Circle shape for female and Square for male) and colors represent survival. I am a gamer and I love contrasting colors of red and green to show the survival. 

* In the bar plot (summarized), it is simply based on ticket price range against a survival rate. Legends with different colors to show Male vs Female survival rate. 


# Feedback.
------------

## The feedback based on first version 'first_index.html'

### Feedback from colleague (Data enthusiast and geek). 

* He identifued that it's a scatter plot which shows info of age vs ticket price. The survivors and non-survivors. 
* Lot of people in the age between 20 to 50. 
* He also noticed that people who pay more had better survival rate.
* He suggested that it can be improved by allowing users to focus on choice based features and neater UI design. 


### Feedback from colleague (Hates programming).

* She described correctly about what the plot is. 
* She also mentioned the relationships and she was able to convey expected info.
* She also conveyed it's a complex graph to convey straightforward info -- while discussing, we came up with idea of using bar plot. 
* She also asked lot of questions related to decision of choosing variables and how the features affect the survival rate. 


### Feedback from a friend (Designer and artist, no computer background).

* She could describe the graph appropriately. 
* She also mentioned the relationships and she was able to convey expected info.
* She was not particularly impressed with UI, suggested some color choices and how it can be neater.
* She also emphasised on making it a simpler graph and again reverted with idea of bar plot.
* She also mentioned to include a caption about the graph, what it does and how you can interact with it.


# Resources.
-------------

* https://github.com/d3/d3/wiki/Gallery
* http://webtasks.keck.waisman.wisc.edu/scatterize/d/Acdck0qHJo#h=2&m=OLS&x=1&y=6
* http://bl.ocks.org/weiglemc/6185069
* https://bl.ocks.org/mbostock/3887051