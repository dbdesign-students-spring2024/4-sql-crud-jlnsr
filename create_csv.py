with open("data/users.csv","r") as file:
    my_list = file.readlines()
    my_list = [i.strip("\n") for i in my_list]

with open("data/usernames.csv","r") as file2:
    my_list2 = file2.readlines()
    my_list2 = [i.strip("\n") for i in my_list2]
    

with open("data/users4.csv","w") as file3:
    for index,(i,j) in enumerate(zip(my_list2,my_list)):
        file3.write(str(index+1)+","+i+","+j+"\n")
