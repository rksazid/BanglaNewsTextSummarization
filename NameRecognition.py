
from nltk.tokenize import word_tokenize, sent_tokenize
import re as regex


def nameRecognition(tokenizeDocument):
    
    ###........... Read from Name File..........
    
    readName = open('./HumanName.txt', 'r', encoding='utf-8')
    HumName = " ".join(readName.readlines())
    Name = set(HumName.split())
    
    
    tokenizeDocument.append('###')
    
    
    
    preName = ["শেখ", "মোঃ","মো", "আবদুল", "মুহাম্মাদ", "চৌধুরী", "জনাব", "সৈয়দ", "মোসাম্মাৎ"  "আবুল", "তালুকদার", "মল্লিক","ডিকস্তা",
    "রোজারিও","আনসারী", "গাজী","চিশতী", "পীর","ফকির","মোল্লা", "মিয়াজী","শাহ","খাজা","ফরাজি","মির্জা","দফাদার","দফাদার","চাকলাদার",
    "ভূঁইয়া","ভূঁঞা", "কাজি", "গোলন্দাজ", "দেওয়ান", "নিয়াজী","খন্দকার" , "পটোয়ারী", "মুন্সী্‌" ,"মুহুরী", "মৃধা", "লস্কর","সরকার","হাজারী","প্রামাণিক্‌",
     "পোদ্দার","সরদার" , "হাওলদার","শিকদার","জোয়ার্দার","ইনামদার","বেগ","লোহানী","ঢালী" ]
    # print(preName[len(preName)-1])
    postName = ["আহমদ", "কবির","মিয়া", "আলী", "খান","মীর", "আরা", "বেগম", "খাতুন", "বড়ুয়া", "আলম", "হাওলাদার", "রহমান", "ইসলাম",
    "উদ্দিন", "কাজী", "হক", "হোসেন", "মোল্লা", "শেখ", "তালুকদার", "গাজী", "চৌধুরী", "মিয়াঁ", "চক্রবর্তী", "বড়ুয়া", "চাক্মা", "হাজারী",
     "সাহা", "ভৌমিক", "রায়", "মণ্ডল", "চন্দ্র", "কুমার", "ভট্টাচার্য", "তেওয়ারি", "চক্রবর্ত্তী", "শর্মা", "দেবনাথ","নাথ‌", "ঠাকুর",""
     "উপাধ্যায়", "গঙ্গোপাধ্যায়","গাঙ্গুলী", "চট্টোপাধ্যায়","চ্যাটার্জি", "বন্দোপাধ্যায়","ব্যানার্জি", "মুখোপাধ্যায়","মুখার্জি", "বাগচী",
    "গোস্বামী","আচার্য্য","ভট্টাচার্য্য" ,"ভট্ট","মৈত্র", "সিদ্দিকী", "সাহা", "মল্লিক", "লাহিড়ী","পান্ডে", "গুপ্ত","মিত্র","সিংহ","রুদ্র","ভদ্র","কর",
    "বিশ্বাস","দে","বসু","বোস","শিকদার","গুহ","রায়","দাশ","নন্দী""চন্দ","দাস","আইচ","নাগ","অধিকারী","আদিত্য","ধর","দত্ত","রক্ষিত","দেব","পালিত",
     "সরকার","সোম","কন্ঠ","ঘোষ","সেন", "মজুমদার","প্রধান","বর্মন","ব্যাপারী","শিকদার","মৃধা","তরফদার","খাঁ","সরকার""কারিগর","কর্মকার","দেওয়ান",
    "পালাকার","পোদ্দার","প্রমাণিক","প্রমাণিক","ভাঁড়", "শীল", "পাটোয়ারি", "পাল","বৈদ্য","হালদার","অধিকারী","গুণ","কুন্ডু","দাসগুপ্ত","বড়াল","কস্তা",
     "ডিকস্তা", "রোজারিও","আনসারী", "গাজী","চিশতী", "পীর","ফকির","মোল্লা", "মিয়াজী","শাহ","খাজা","ফরাজি","মির্জা","দফাদার","দফাদার","চাকলাদার",
    "ভূঁইয়া","ভূঁঞা", "কাজি", "গোলন্দাজ", "দেওয়ান", "নিয়াজী","খন্দকার" , "পটোয়ারী", "মুন্সী‌" ,"মুহুরী", "মৃধা", "লস্কর","সরকার","হাজারী","প্রামাণিক‌",
     "পোদ্দার","সরদার" , "হাওলদার","শিকদার","জোয়ার্দার","ইনামদার","বেগ","লোহানী","ঢালী" , "মাতুব্বর", "নবী", ]
    
    #print(postName)
    NameList = []
    
    CopyDocument = tokenizeDocument
    
    flag = 1
    for i in tokenizeDocument:
        if i in preName:
            flag = 1
            pos = tokenizeDocument.index(i)
            strName = CopyDocument[pos]
            tokenizeDocument[pos] = '@@@'
            while flag:
                if tokenizeDocument[pos + 1] in Name:
                    strName = strName + " " + CopyDocument[pos + 1]
                    tokenizeDocument[pos+1] = '@@@'
                    pos = pos + 1
                else:
                    # print(strName)
                    flag = 0
                    NameList.append(strName)
                    strName = []
    #print(NameList)
    
    NameList1 = []
    
    #CopyDocument1 = word_tokenize(strDocument)
    #tokenizeDocument1 = CopyDocument1
    #print(tokenizeDocument)
    
    flag1 = 1
    for i in tokenizeDocument:
        if i in postName:
            flag1 = 1
            pos = tokenizeDocument.index(i)
            strName1 = CopyDocument[pos]
            tokenizeDocument[pos] = '@@@'
            while flag1:
                if tokenizeDocument[pos - 1] in Name:
                    strName1 = strName1 + " " + CopyDocument[pos - 1]
                    tokenizeDocument[pos-1] = '@@@'
                    pos = pos - 1
                else:
                    flag1 = 0
                    inputWords = strName1.split(" ")
                    inputWords = inputWords[-1::-1]
                    output = ' '.join(inputWords)
                    NameList1.append(output)
        else:
            pos = tokenizeDocument.index(i)
    
            tokenizeDocument[pos] = i
    #print(NameList1)
    #print(tokenizeDocument)
    
    NameList2 = []
    for i in tokenizeDocument:
        if i in Name:
            flag = 1
            pos = tokenizeDocument.index(i)
            strName2 = CopyDocument[pos]
            tokenizeDocument[pos] = '@@@'
            while flag:
                if tokenizeDocument[pos + 1] in Name:
                    strName2 = strName2 + " " + CopyDocument[pos + 1]
                    tokenizeDocument[pos+1] = '@@@'
                    pos = pos + 1
                else:
                    # print(strName)
                    flag = 0
                    NameList2.append(strName2)
                    strName2 = []
    
    #print(NameList2)
    
    NameList3 = NameList+ NameList1+ NameList2
    #print(NameList3)
    return NameList3
