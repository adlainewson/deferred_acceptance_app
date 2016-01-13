
# coding: utf-8

# In[8]:

#!/usr/bin/env python3

print('Content-type: text/html')

## This is the website for illustrating the DA algorithm in 1:1 matching
# code is written by Adlai Newson; http://adlainewson.info
# email adlai dot newson at gmail dot com

from numpy import array,empty,zeros,ones,array_equal
from random import shuffle

import cgi, cgitb 

## comment out the below and specify m,w manually if you want to run this independently
#form = cgi.FieldStorage() 
#w = int(form.getvalue('women'))
#m  = int(form.getvalue('men'))
    
m = 2 # number of men in the game
w = 3 # number of women in the game



# In[9]:

## Functions for printing the webpage

tablecss = "border-collapse:collapse;border-spacing:0"
cellcss = "font-family:Arial, sans-serif;font-size:16px;padding:30px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;"
s = '../deferred_acceptance/' #path string to where the slides code is
def start_slides():
    ''' Opening HTML and script '''
    print('''
    <html>
    <head>
      <meta charset="utf-8">
      <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
      <meta name="viewport" content="width=1024, user-scalable=no">

      <title>Deferred Acceptance in the Marriage Market</title>

      <link rel="stylesheet" media="screen" href="%score/deck.core.css">

      <link rel="stylesheet" media="screen" href="%sextensions/goto/deck.goto.css">
      <link rel="stylesheet" media="screen" href="%sextensions/menu/deck.menu.css">
      <link rel="stylesheet" media="screen" href="%sextensions/navigation/deck.navigation.css">
      <!-- <link rel="stylesheet" media="screen" href="%sextensions/status/deck.status.css"> -->
      <link rel="stylesheet" media="screen" href="%sextensions/scale/deck.scale.css">

      <!-- Style theme. More available in /themes/style/ or create your own. -->
      <link rel="stylesheet" media="screen" href="%sthemes/style/swiss.css">

      <link rel="stylesheet" media="screen" href="%sthemes/transition/fade.css">

      <link rel="stylesheet" media="print" href="%score/print.css">

      <script src="%smodernizr.custom.js"></script>
    </head>
    <body>
      <div class="deck-container">
  ''' % (s,s,s,s,s,s,s,s,s,s))
def end_slides():
    ''' Closes out the webpage '''
    print('''
        <div aria-role="navigation">
          <a href="#" class="deck-prev-link" title="Previous">&#8592;</a>
          <a href="#" class="deck-next-link" title="Next">&#8594;</a>
        </div>
        <!--
        <p class="deck-status" aria-role="status">
          <span class="deck-status-current"></span>
          /
          <span class="deck-status-total"></span>
        </p>
        -->

        <form action="." method="get" class="goto-form">
          <label for="goto-slide">Go to slide:</label>
          <input type="text" name="slidenum" id="goto-slide" list="goto-datalist">
          <datalist id="goto-datalist"></datalist>
          <input type="submit" value="Go">
        </form>

      </div>

    <script src="%sjquery.min.js"></script>
    <script src="%score/deck.core.js"></script>

    <script src="%sextensions/goto/deck.goto.js"></script>
    <!-- <script src="%sextensions/status/deck.status.js"></script> -->
    <script src="%sextensions/navigation/deck.navigation.js"></script>

    <script>
      $(function() {
        $.deck('.slide');
      });
    </script>
    </body>
    </html>
    ''' % (s,s,s,s,s))
    
def open_slide():
    ''' Starts a new slide '''
    print("<section class='slide'>\n")
    print('''
   <p style='font-family:Arial,sans-serif;font-size:24px'>
        Deferred Acceptance in the Marriage Market
   </p>
   <p style='font-family:Arial,sans-serif;font-size:12px'>
        This is an implementation of the deferred acceptance algorithm in the marriage market.<br>
	This is the men-proposing version, preferences are generated randomly, and everyone prefers any match
	to no match.<br>
	Men are on the column players, women are the row players, and the rankings in the cells are in the usual row,column order. <br>
        Hit the right cursor to advance. Once every man has had a chance to propose, the next round is triggered.<br>
    <br>
       For source code et al, see my homepage www.[].com; you can email me at adlai dot newson at gmail.com.
    </p>
    <p style='font-family:Arial;font-size:20px'><b>
    ''')
    print("Round: ",str(rounds), '</b>')
    
def close_slide():
    ''' Closes the slide '''
    print("</section>\n")
          
def print_table():
    ''' Prints the table with preferences and background colors '''
    print("<br><br><p align=left><table style='",tablecss,"'>\n")
    for i in range(len(women)):
        for j in range(len(men)):
            if j == 0:
                print("  <tr>\n")
            if j == m:
                print("  </tr>\n")
            print("    <td style='",cellcss,"background-color:",color_convert(i,j),"'>\n")
            print("      ( ", int(prefs_mat_women[i][j]), ",", int(prefs_mat_men[i][j]), " )\n")
            print("    </td>\n")
    print("</table></p>\n")

def print_slide():
    open_slide()
    print_table()
    close_slide()


# In[52]:

# The DA code


def color_convert(i,j):
    'Convert status to appropriate colour'
    if colormat[i][j] == 0:
        return 'white'
    if colormat[i][j] == 1:
        return 'lightgreen'
    if colormat[i][j] == 2:
        return 'indianred'

def prefs_matrices():
    'Generate the preference matrix'
    for i in range(len(women)):
        for j in range(len(men)):
            prefs_mat_men[i][j] = men[j].prefs.index(i) + 1
            prefs_mat_women[i][j] = women[i].prefs.index(j) + 1


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
        print_slide()
            


def deferred_accept(girl,guy):
    colormat[women.index(girl),men.index(guy)] = 1

def reject(girl,guy):
    colormat[women.index(girl),men.index(guy)] = 2

    
m, w = 2, 3;

randomize_prefs = 0;
if randomize_prefs == 1:
    # If preferences are not specified, just generate random preferences
    def prefshuffle(prefs):
        b = prefs[:]
        shuffle(b)
        return b
    wprefs = [i for i in range(m)]
    mprefs = [i for i in range(w)]
    men, women = [], []
    for i in range(m):
        men.append(Man(prefshuffle(mprefs)))
    for j in range(w):
        women.append(Woman(prefshuffle(wprefs)))
else:
    men, women = [], []
    if True:
        # debugging
        m_prefs = [[1,2,3],[3,2,1]]
        w_prefs = [[1,2],[1,2],[2,1]]
    
    # these two lines shift preferences to start at 0
    w_prefs = [[i-1 for i in j] for j in w_prefs]
    m_prefs = [[i-1 for i in j] for j in m_prefs]
    
    for i in range(m):
        men.append(Man(m_prefs[i]))
    for j in range(w):
        women.append(Woman(w_prefs[i]))




for man in men:
    man.initialize()
for woman in women:
    woman.initialize()

prefs_mat_men, prefs_mat_women  = zeros((w,m)), zeros((w,m))    
prefs_matrices()


# In[ ]:

## Running the algo

colormat = zeros((len(women),len(men)))

sadmen = 1
rounds = 0

start_slides()
print_slide()

while sadmen > 0:
    sadmen = 0
    rounds += 1
    colormat_old = colormat
    for man in men:
        man.activate()
    for man in men:
        if not man.match:
            sadmen += 1

end_slides()

