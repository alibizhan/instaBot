from userInfo import theirUsername 
userFollowing = []
userFollowers = []
list_difference = []

followingFile = theirUsername+"Following.txt"
followerFile = theirUsername+"Followers.txt"
notFollwers = theirUsername+"_fans.txt"
notFollowing = theirUsername+"_notFollowing.txt"
with open(followingFile, "r",encoding="utf-8") as file:
    for item2 in file:
        userFollowing.append(item2)


with open(followerFile, "r",encoding="utf-8") as file:
    for item in file:
        userFollowers.append(item)




list_difference = []
choice = int(input("Enter 1 for notFollowing and 2 for fans :\n"))
if(choice == 1):
    for item in userFollowing:
        if item not in userFollowers:
            print(item)
            list_difference.append(item)
else:
    for item in userFollowers:
        if item not in userFollowing:
            print(item)
            list_difference.append(item)
print(len(list_difference))


if(choice==1):

    with open(notFollowing, "w", encoding="UTF-8") as file:
        for item in list_difference:
            file.write(str(item))
else:
    with open(notFollwers, "w", encoding="UTF-8") as file:
        for item in list_difference:
            file.write(str(item))