import pandas as pd
import numpy as np
import json as js
import math

#COMPUTE P(a_i,a_j|c) from D
def calc_cond_prob(dataset,up,down = []):

    query_up = []
    query_down = []

    for i in up:
        query_up.append(i + ' == \"' + up[i] + "\" ")

    for i in down:
        query_down.append(i + ' == \"' + down[i] + "\" ")

    query_up = query_up + query_down

    query_up = (" & ".join(query_up))
    query_down = (" & ".join(query_down))

    if(not query_down):
        return (len(dataset.query(query_up))/len(dataset))

    return (len(dataset.query(query_up))/len(dataset.query(query_down)))

def calc_info_gain(dataset, var1, var2, var3):

    sumval = 0
    var1_values = dataset[var1].unique()
    var2_values = dataset[var2].unique()
    var3_values = dataset[var3].unique()

    for i in var1_values:
        for j in var2_values:
            for k in var3_values:

                p_xyz = (calc_cond_prob(dataset, {var1 : i, var2: j, var3: k}))
                p_xy_z = (calc_cond_prob(dataset,{var1 : i, var2: j}, {var3: k} ))
                p_x_z = (calc_cond_prob(dataset,{var1 : i}, {var3: k}))
                p_y_z = (calc_cond_prob(dataset,{var2 : j}, {var3: k}))

                if(p_xy_z == 0):
                    sumval = sumval + (p_xyz)
                elif(p_x_z == 0 or p_y_z == 0):
                    sumval = sumval + (p_xyz * math.log(p_xy_z/0.00001))
                else:
                    sumval = sumval + (p_xyz * math.log(p_xy_z/(p_x_z * p_y_z)))


    return sumval

    def calcula_cpd(dataset, weights_pair, var, classvar):
        


def main(filepath, classvar):

    #A SET D OF TRAINING EXAMPLES
    dataset = pd.read_csv(filepath)

    #COMPUTE P(C) FROM D
    classes = dataset[classvar].unique()
    value_counts = dataset[classvar].value_counts()
    p_c = {}
    for i in classes:
        p_c[i] = value_counts[i]/len(dataset)

    info_gains = {}
    weights_single = {}
    weights_pair = {}

    print("Calculando ganhos de informação...")

    try:
        with open("./" + filepath.split("/")[-1] + '.json', 'r') as f:
            info_gains = js.load(f)
        print("Arquivo já existente. Carregando valores..")
    except:
        n_inter = len(dataset.columns) * len(dataset.columns)
        n_inter_atual = 0

        for i in dataset.columns:
            for j in dataset.columns:
                n_inter_atual = n_inter_atual + 1
                if(n_inter_atual % 10 == 0):
                    prog = (n_inter_atual/n_inter)*100
                    print("Progresso: ", n_inter_atual, " de ", n_inter, "(",  int(prog), "%)" )

                if(str(j + " " + i) not in info_gains):
                    info_gains[i + " " + j] = calc_info_gain(dataset, i,j,classvar)
                else:
                    info_gains[i + " " + j] = info_gains[j + " " + i]
        
        json = js.dumps(info_gains)
        f = open(filepath.split("/")[-1] + '.json',"w")
        f.write(json)
        f.close()

    #Compute Wi
    #Compute Wij
    
    print("Calculando pesos single...")
    for i in dataset.columns:
        sum_val = 0
        for j in dataset.columns:
            if(not j == i and not j == classvar and not i == classvar):
                sum_val = sum_val + info_gains[i + " " + j]
        weights_single[i] = sum_val

    print("Calculando pesos par...")
    for i in dataset.columns:
        for j in dataset.columns:
            if(not j == i and not j == classvar and not i == classvar):
                if(weights_single[i] == 0):
                    weights_pair[i + " " + j] = info_gains[i + " " + j]
                else:
                    weights_pair[i + " " + j] = info_gains[i + " " + j]/weights_single[i]

    
    
    

if __name__ == "__main__":
    main("./resources/final.csv","i_mudadecubito")

