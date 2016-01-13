
# coding: utf-8

# In[59]:

# Deferred acceptance in the marriage market, Adlai Newson
#
#    - preferences are random
#    - nobody prefers to be alone
#


from numpy import array,empty,zeros
from random import shuffle
#import HTML

class Man:
    def __init__(self,preferences):
        self.prefs = preferences
        self.match = False; 
        self.last_offer_to = False
        self.target = 0
        
    def initialize(self):
        self.wlist = []
        for i in self.prefs:
            self.wlist.append(women[i])
  
    def activate(self):
        if self.match:
            pass
        else:
            if self.target < len(self.prefs):
                self.last_offer_to = women[self.prefs[self.target]]
                self.target +=1
                self.match = self.last_offer_to
                self.last_offer_to.receive_offer(self)
            else:
                self.match=self

    def receive_rejection(self):
        self.match = False
    

class Woman:
    def __init__(self,preferences):
        self.prefs = preferences
        self.current_match = None
        
    def initialize(self):
        self.mlist = []
        for i in self.prefs:
            self.mlist.append(men[i])        
            
    def prefers(self,guy):
        if self.current_match == None:
            deferred_accept(self,guy)
            return True
        else:
            if self.mlist.index(guy) < self.mlist.index(self.current_match):
                return True
            else:
                return False
            
    def receive_offer(self,guy):
        if self.prefers(guy):
            if self.current_match != None:
                deferred_accept(self,guy)
                reject(self,self.current_match)
                self.current_match.receive_rejection()
            self.current_match = guy
            
        else:
            guy.receive_rejection()
            reject(self,guy)
            
def prefshuffle(prefs):
    b = prefs[:]
    shuffle(b)
    return b

def deferred_accept(girl,guy):
    colormat[women.index(girl),men.index(guy)] += 1

def reject(girl,guy):
    colormat[women.index(girl),men.index(guy)] += 2

    
# Set the parameters here
m = 4 # number of men in the game
w = 3 # number of women in the game

wprefs = [i for i in range(m)]
mprefs = [i for i in range(w)]

men, women = [], []
for i in range(m):
    men.append(Man(prefshuffle(mprefs)))
for j in range(w):
    women.append(Woman(prefshuffle(wprefs)))


for man in men:
    man.initialize()
for woman in women:
    woman.initialize()
    
colormat = zeros((len(women),len(men)))
print("Legend:")
print(" "*10, "0 : nothing sent or received")
print(" "*10, "1 : i deferred accepts j")
print(" "*10, "2 : i rejects j")
print(" "*10, "3 : i rejects j, who was previously DA")
print()


sadmen = 1
rounds = 0

#preferences_matrix = array((len(women),len(men)))
#preferences_matrix = [[],[]]
#for man in men:
#    for woman in women:
#        guys_opinion = man.wlist.index(woman)
#        girls_opinion = woman.mlist.index(man)
#        preferences_matrix.append((girls_opinion,guys_opinion))
#    print(preferences_matrix[i])
#print(preferences_matrix)

while sadmen > 0:
    sadmen = 0
    print("ROUND ", rounds)
    for man in men:
        man.activate()
    for man in men:
        if not man.match:
            sadmen += 1
    print(colormat)
    print()
    #color_graph(colormat)
    rounds += 1

print()
print("Conclusion:")
for man in men:
    if man.match != man:
        print(" "*10, "Man", men.index(man), "is matched with woman", women.index(man.match))
    else:
        print(" "*10, "Man", men.index(man), "is matched with himself")
for woman in women:
    if woman.current_match == None:
        print(" "*10, "Woman", women.index(woman),"is matched with herself")





# In[55]:

## this is a work in progress for HTML coloring

#def color_graph(mat):
#    print_prefs_mat = [[],[]]
#    print_color_mat = [[],[]]
#    for i in range(len(women)):
#        for j in range(len(men)):
#            #printmat[i,j]=str((men[i].[women[j]]))
#            pass
        
#myarray = [[(1,1),str((2,2))],[str((3,3)),str((4,4))]]
#print(myarray)


#example_table = [[str(i for i in range(j,j+len(men))] for j in range(0,30,10)]

