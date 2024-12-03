import ollama
import random
import copy
import sys
import subprocess
import numpy as np
def install_mpl():
    print("NOTE: INSTALLING MATPLOTLIB!")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "matplotlib"])
try:
    import matplotlib.pyplot as plt
except:
    install_mpl()
    import matplotlib.pyplot as plt

#opens a txt file, feeds lines into an array, returns that array
def open_txt_read(txt):
    txtFile = open(txt,"r",encoding="utf-8")
    txt = []
    for line in txtFile:
        line = line.rstrip('\n')
        txt.append(line)
    txtFile.close()
    return txt

#opens a txt file and writes to it.
def write_to_txt(comments,txt):
    n = 1
    results_file = open(txt,"w",encoding="utf-8")
    for element in comments:
        for elementA in element:
            results_file.write(f'{str(elementA)}\n')
        n+=1
    results_file.close()

#gives a prompt to phi3-mini and returns the response.
def get_response(prompt):
    resp = ollama.generate(model="phi3:mini",prompt=prompt)
    return (resp["response"])
    a = random.randint(1,3)

if __name__ == "__main__":
    #sys.argv[1] = output text file     sys.argv[2] = output graph file     #sys.argv[3+] = text files
    strResp = "MESSAGE: IN ONE WORD ONLY, is the following message Positive, Negative, or Neutral: "
    print("Opening comment files...")
    comments = []
    for i in range(3,len(sys.argv)):
        comments.append(open_txt_read(sys.argv[i]))
    responses=[]
    tArr = []
    print("Finished opening comment files!")
    print("Feeding comments to Phi-3 mini...")
    for element in comments:
        for elementA in element:
            string = strResp + elementA + "\""
            tArr.append(get_response(string))
        responses.append((copy.copy(tArr)))
    print("Finished getting responses from Phi-3 mini!")
    print("Writing to text file(s)...")
    n = 1
    for element in responses:
        name= sys.argv[1] +"_" + str(n) + ".txt"
        write_to_txt(responses,name)
        n=n+1
    print(f"Finished writing to text file(s)!")
    rVist = []
    print(f'Graphing...')
    for element in responses:
        #0 = Positive       1 = Negative        2 = Neutral
        rt = [0,0,0]
        for elementA in element:
            if("positive" in elementA.lower()):
                rt[0] +=1
            elif("negative" in elementA.lower()):
                rt[1] +=1
            else:
                rt[2] +=1
        rVist.append(copy.copy(rt))

    x = np.array(range(1,len(rVist)+1))
    y1 = []#pos
    y2 = []#neg
    y3 = []#neu
    for element in rVist:
        y1.append(element[0])
        y2.append(element[1])
        y3.append(element[2])
    plt.bar(x-0.2,y1,width=0.2,color='cyan')
    plt.bar(x,y2,width=0.2,color='blue')
    plt.bar(x+0.2,y3,width=0.2,color='purple')
    plt.xlabel("Product")
    plt.ylabel("Number of Reviews")
    plt.legend(["Positive","Negative","Neutral"])
    plt.savefig(f'{sys.argv[2]}.png')
    print(f'Finished graphing! Output graph to"{sys.argv[2]}.png"')
    print("Script finished running.")

