# coding=utf-8
import json
import string
import readFromFile
import sys

students = ""
TOEFL = ['TOEFL', 'toefl', 'IELTS', 'ielts', '托福', '雅思']
Kaoyan = ['考研']
Programming = ['c++', 'java', 'JAVA', '编程', 'C++', 'PHP', 'php', 'html', 'HTML', 'web', 'Web', 'WEB', "代码", '算法']

if sys.argv[1] == 'train':
    lines = readFromFile.readLines('../studentForm/train/borrow_train_invert.txt')
elif sys.argv[1] == 'test':
    lines = readFromFile.readLines('../studentForm/test/borrow_test_invert.txt')
else:
    print 'Invalid arguments'

"""
    注：有些图书的编号缺失。字段描述和示例如下（第三条记录缺失图书编号）：
    学生id，借阅日期，图书名称，图书编号
    9708,2014/2/25,"我的英语日记/ (韩)南银英著 (韩)卢炫廷插图","H315 502"
    6956,2013/10/27,"解读联想思维: 联想教父柳传志","K825.38=76 547"

统计是否结果书，是否借过考研书，是否借过编程书，是否借过托福书
统计这些类别书的数量，还统计了不同种类书的数目
"""
for line in lines:
    features = {"stuId":-1, "ifBorrowed":0, "numOfBorrowed":0, 
            "timesOfTOEFL":0, "timesOfKaoyan":0, "timesOfProg":0, "numOfCateBorrowed":0}
    # Add category A-Z number counters to dic features
    # 用于统计书的类别
    for i in list(string.ascii_uppercase):
        if i == 'T' and i != 'L' and i != 'M' and i != 'W' and i != 'Y':
            features["numInCate" + i] = 0
    books = line.split('$')
    features['stuId'] = int(books[0])
    # 统计是否借书，借书的数量，考研，托福，编程，数类别的数量
    if len(books) > 1:
        features['ifBorrowed'] =  1 
        features['numOfBorrowed'] = len(books) - 1
        for i in range(1, len(books)):
            # filter out the "..." signs in the string.
            items = books[i].strip().split('\",\"')
            if len(items) < 3:
                continue
            print items
            time     = items[0][1:]
            bookName = items[1]
            bookISBN = items[2][:-1]
            # Count category A-Z borrowed times. 
            if bookISBN[0] == 'T' and bookISBN[0] in string.ascii_uppercase:
                features["numInCate" + bookISBN[0]] += 1
            # Count times of toefl books, KaoYan books and Programming books.
            for each in TOEFL:
                if each in bookName:
                    features['timesOfTOEFL'] += 1
                    break
            for each in Kaoyan:
                if each in bookName:
                    features['timesOfKaoyan'] += 1
                    break
            for each in Programming:
                if each in bookName:
                    features['timesOfProg'] += 1
                    break
            
        # Count the number of distinct categories this person has borrowed.
        # 统计不同种类书的数目
        for i in list(string.ascii_uppercase):
            if i == 'T' and i != 'L' and i != 'M' and i != 'W' and i != 'Y':
                features['numOfCateBorrowed'] += 0 if features['numInCate' + i] == 0 else 1 
        
    #students.append(json.dumps(features, sort_keys=True))
    students += json.dumps(features, sort_keys=True) + '\n'
        
with open(sys.argv[1] + 'Processed/BorrowProcessed.txt', 'w') as fw:
    fw.write(students)
