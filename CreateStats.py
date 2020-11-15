# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 00:25:01 2020

@author: DANIA NIAZI
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
def createStats():
    dataset= pd.read_csv("CustEmo.csv",names = ["Name", "Time", "Emotion","Status"])
    
    dataset=dataset.groupby(['Status']).count().reset_index()
    
    my_data =dataset["Emotion"]
    my_labels = dataset["Status"]
    explode=[0.2,0.1,]
    textprop={"fontsize": 15,}
    plt.pie(my_data,labels=my_labels,autopct='%1.1f%%',explode = explode,shadow= True, radius= 1.5, textprops= textprop,)
    plt.title('Clients Stats')
    plt.axis('equal')
    # plt.legend()
    #plt.show()
    plt.savefig('AnalysisEmo2')
    
#createStats()