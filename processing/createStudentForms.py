import sys
import readFromFile

"""
没有用 pandas 有点伤
按照学生 id 进行特征统计，所有相同学生的记录合并到一个 stuId 中
"""
def invertForm(filePath):
    students = {}
    lines = readFromFile.readLines(filePath)
    for each in lines:
        l = each.strip().split(',', 1)
        stuId = int(l[0])
        if stuId in students:
            students[stuId] += "$" + l[1]
        else:
            students[stuId] = l[1]
    ret = ""
    for key, value in students.iteritems():
        ret += str(key) + "$" + value + '\n'
    fw = open("../studentForm/test/" + filePath.split('/')[-1].split('.')[0] + "_invert.txt", 'w')
    fw.write(ret)
    fw.close()

if __name__=='__main__':
    invertForm('../data/test/' + sys.argv[1])
    
