n=int(input("Enter the size of forest: "))
forest=[]
print("Enter the values of 0s and 1s: ")

for i in range(n):
    row=list(map(int,input().split()))
    forest.append(row)

m=int(input("Enter the Extraction Zone grid size: "))

x,y=map(int,input("Enter the mid point: ").split())

half=m//2
start_row=x-half
end_row=x+half+1
start_col=y-half
end_col=y+half+1
zone=[]
for r in range(start_row,end_row):
    temp=[]
    for c in range(start_col,end_col):
        temp.append(forest[r][c])
    zone.append(temp)
tree=0
for r in zone:
    for num in r:
        if num==1:
            tree+=1
print("OUTPUT\n")
print(f"Centre:{x,y}\n")
print(f"Extraction Zone {m,m}")
for r in zone:
    print(r)
print("\n")
print(f"Number of trees: {tree}")
