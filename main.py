import pandas as pd

def main(filepath, classvar):
    #A SET D OF TRAINING EXAMPLES
    dataset = pd.read_csv(filepath)

    #COMPUTE P(C) FROM D
    classes = dataset[classvar].unique()
    value_counts = dataset[classvar].value_counts()
    p_c = {}
    for i in classes:
        p_c[i] = value_counts[i]/len(dataset)
    print(p_c)
    
    

if __name__ == "__main__":
    main("./resources/final.csv","i_mudadecubito")

