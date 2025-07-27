import tkinter as tk

class HistogramApp:

    def __init__(self,window,task1,task2,date):         #initialize the graphic with tkinter root
        self.window = window
        self.window.title("Histrogram")                 #add tittle name
        self.date  = date                               #date for the title above

        self.task1 = task1                              #first datedefine
        self.task2 = task2                              #second datadefine

        self.Canvas_width = 1200                        #full width of the Canvas
        self.Canvas_height = 400                        #full height of the Canvas
        self.padding = 100                              #margin around the content

        #define barchart properties
        self.width = 15                                 #width of individuals bar
        self.bar_gap = 0                                #gap between the bar is 0
        self.groupspacing = 15                          #space between different bargroups
        self.bargraph_width = 0

        self.max_value = max(max(self.task1.values()), max(self.task2.values()))        #find the max of dataset
        self.measure = (self.Canvas_height-2*self.padding) / self.max_value             #measure bars to fit Canvas height

        #define colors
        self.textcolor = "#747673"                      #color for text
        self.firstbarcolor = "#95fb97"                  #color for first dataset bar
        self.secondbarcolor = "#ff9496"                 #color for second dataset bar

        #make a canva to draw the graph
        self.Canvas = tk.Canvas(
            self.window,
            width = self.Canvas_width,
            height = self.Canvas_height,
            background = "#edf2ee"                      #Light color for background
        )

        self.Canvas.pack()                              #add it to tk window


        #draw all of the bar chart
        self.createbars()                               #Draw the bars for datasets
        self.createaxes()                               #Draw the x-axis
        self.createlegend()                             #Add legend to the datasets
        self.createfooter_text()                        #Add footertext to bars


    def createaxes(self):
    #Draw the x-ais
        self.Canvas.create_line(
            self.padding + self.groupspacing,             #start x-axis padding left
            self.Canvas_height - self.padding,            # y-coordinate at the bottom
            self.bargraph_width,                        #barchart width
            self.Canvas_height - self.padding,            #same y-coordinate of the horizontal line
            width = 1,
            fill = 'black'                              #black axis line
              )
        

    def createbars(self):
    #draw first bar
        x = self.padding + self.groupspacing            #starting x-coordinate for first group
        x2 = 0                                          #position of the last bar


        for label in self.task1.keys():
            #bar for task1
            startingvalue = self.task1[label]
            bar_peak1 = startingvalue*self.measure
            x1 = x
            y1 = self.Canvas_height-self.padding                 #Base of bar
            x2 = x + self.width
            y2 = self.Canvas_height-self.padding-bar_peak1       #top of bar
            self.Canvas.create_rectangle(x1,y1,x2,y2,outline = "black", fill = self.firstbarcolor) #craete and Draw rectangle
            self.Canvas.create_text((x1+x2)/2,y2-10,text =str(startingvalue),fill = "#54bc52",font = ("Arial",10,"bold") )   #top of the bar value


            #Second datasets bar
            endingvalue = self.task2[label]
            bar_peak2 = endingvalue*self.measure
            x1_2=x2                                             #satars of the first bar ends
            x2_2 = x1_2+ self.width
            y2_2=self.Canvas_height-self.padding-bar_peak2
            self.Canvas.create_rectangle(x1_2,y1,x2_2,y2_2,outline="black",fill=self.secondbarcolor)
            self.Canvas.create_text((x1_2+x2_2)/2,y2_2-10,text=str(endingvalue),fill="#ec7057",font=("Arial",10,"bold"))  #top of the bar value


            #Group label of bars
            self.Canvas.create_text(
                (x + x2_2 ) /2,
                self.Canvas_height-self.padding+15,
                text = "{:02d}".format(label),                  #two digits format
                font = ("Arial",12,"bold"),
                fill = "black",
                )
            

             #x-coordinate to the next group moving        
            x = x + 2* self.width+self.groupspacing
        #self.bargraph_width = x2 = self.width
        self.bargraph_width = x

        
    def createlegend(self):
        legend_xbeging = 20              # strat x-coordinate for legend
        legend_ybegin = 50               # strat y-coordinate for legend

        #chart title
        self.Canvas.create_text(
            legend_xbeging + 20,
            legend_ybegin -30,
            text = "Histrogram of Vehicle Frequency per Hour({})".format(self.date),
            anchor = "w",                #Align text to left
            font = ("Arial",24,"bold"),
            fill = self.textcolor,
            )
        
        #legend entry of first dataset    
        self.Canvas.create_rectangle(
            legend_xbeging,legend_ybegin+20,legend_xbeging+20,legend_ybegin,outline = "black",fill = self.firstbarcolor)
            
        self.Canvas.create_text(
            legend_xbeging +25,legend_ybegin+10,text="Elm Avenue/Rabbit Road",anchor = "w",font = ("Arial",12,"bold"),fill = self.textcolor)
        
        #legend entry of first dataset 
        self.Canvas.create_rectangle(
            legend_xbeging,legend_ybegin+30,legend_xbeging+20,legend_ybegin+50,outline = "black",fill = self.secondbarcolor)

        self.Canvas.create_text(
            legend_xbeging+25,legend_ybegin+40,text = "Hanley Highway/Westway",anchor = "w",font = ("Arial",12,"bold"),fill = self.textcolor)
                
                                    
    def createfooter_text(self):
        self.Canvas.create_text(
            self.Canvas_width/2,                            #centerd of horizontally
            self.Canvas_height -self.padding+50,            #a little bellow the x-axis
            text = "Hours 00:00 to 24:00",                  #Footer text
            fill = self.textcolor,
            font = ("Arial",14,"bold"),
            )                              
                
 
            
            

        



