import os

cwd = os.getcwd()
directory = cwd + "/../rsc/malopolskie/"

searcheID = "Sprzedam rodzinny, wygodny, 7 osobowy samochód Opel Zafira Lift 1.8 benzyna 125 KM Samochód w bardzo"
i = 1

for filename in os.listdir(directory):
    print(str(i/500) + "%")
    i = i +1
    for offerFileName in os.listdir(directory + filename + "/offers/"):
        fileFullPath = directory + filename + "/offers/" + offerFileName
        html = open(fileFullPath, "r").read()
        if(searcheID in html):
            print(fileFullPath)
            print("found")

print("finish")
    #  filename = e.g. slaskie
    # for file in os.listdir(directory + filename + "/"):
    #     # file = e.g. 1
    #     features_directory = directory + filename + "/" + file + "/features/"
    #     os.makedirs(features_directory, exist_ok=True)
    #     currentDir = directory + filename + "/" + file + "/offers/"
    #     i += 1
    #     print(currentDir + " number: " + str(i))
    #     try:
    #         for item in os.listdir(currentDir):
    #             currentFilePath = currentDir + item
    #             html = open(currentFilePath, "r").read()
    #             if(os.path.isfile(features_directory + item)):
    #                 continue
    #             else:
    #                 features_json = extractFeatures(html)
    #                 with open(features_directory + item, 'w') as outfile:
    #                     json_str = str(features_json)
    #                     outfile.write(json_str)
    #     except (FileNotFoundError):
    #         continue