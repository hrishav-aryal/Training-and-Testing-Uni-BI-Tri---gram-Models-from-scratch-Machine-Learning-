# Hello World program in Python
import math


def padFile(file, filenew):
    f = open(file, "r", encoding="utf8")
    newFile = open(filenew, "a", encoding="utf8")
    line = f.readline()
    while line != "":
        l = "<s> "
        line = line.rstrip('\n')
        line = line.lower()
        l += line + " </s>"
        newFile.write(l + '\n')
        line = f.readline()


def replaceWithUnk(file, newfile):
    fr = open(file, 'r')
    fr1 = open(file, 'r')
    fw = open(newfile, 'a')
    dic = dict()

    for line in fr:
        l1 = line.rstrip("\n")
        l = l1.split(" ")
        for word in l:
            if dic.__contains__(word):
                d = {word: dic.get(word) + 1}
                dic.update(d)
            else:
                dic.__setitem__(word, 1)

    for linee in fr1:
        line1 = linee.rstrip('\n')
        sp = line1.split(' ')
        for word in sp:
            if dic.get(word) > 1:
                fw.write(word)
                fw.write(" ")
            else:
                fw.write('<unk> ')
                # print(word)
        fw.write("\n")


def unigramTrainModel(dictionary, total):
    unigram_prob = dict()
    for word in dictionary:
        p = dictionary.get(word) / total
        unigram_prob.__setitem__(word, p)
    return unigram_prob


def bigramTrainModel(dictionary, total):
    bigram_prob = dict()
    for biword in dictionary:
        p = dictionary.get(biword) / total
        bigram_prob.__setitem__(biword, p)
    return bigram_prob


def bigramSmoothingTrainModel(dictionary, total):
    bigram_prob_s = dict()
    for biword in dictionary:
        p = (dictionary.get(biword) + 1) / (total + len(dictionary))
        bigram_prob_s.__setitem__(biword, p)
    return bigram_prob_s


def unigramDictionary(file):
    fr = open(file, 'r')
    dic = dict()

    for line in fr:
        line = line.rstrip('\n')
        l = line.split(" ")
        for word in l:
            if dic.__contains__(word):
                d = {word: dic.get(word) + 1}
                dic.update(d)
            else:
                dic.__setitem__(word, 1)
    return dic


def biDictionary(file):
    fr = open(file, 'r')
    dic = dict()

    for line in fr:
        line = line.rstrip('\n')
        l = line.split(" ")
        word_count = 0;
        biword = ''
        tempword = ''

        for word in l:
            word_count += 1
            biword = biword + tempword + word
            if word_count == 2:
                tempword = word
                if dic.__contains__(biword):
                    d = {biword: (dic[biword] + 1)}
                    dic.update(d)
                else:
                    dic.__setitem__(biword, 1)
                word_count = 1
                biword = ""

    return dic


def totalUniWordtokens(dictionary):
    count = 0
    for freq in dictionary.values():
        count += freq
    return count


def calc_wordtype_percent(uniword_train_dict, uniword_test_dic):
    notoccur_count = 0
    for word in uniword_test_dic:
        if word in uniword_train_dict.keys():
            continue
        else:
            notoccur_count += 1

    return (notoccur_count / len(uniword_test_dic)) * 100


def calc_wordtoken_percent(uniword_train_dict, uniword_test_dic):
    notoccur_count = 0
    total = 0
    for word in uniword_test_dic:
        if word not in uniword_train_dict.keys():
            notoccur_count = notoccur_count + uniword_test_dic[word]
            #print(word)

        total = total + uniword_test_dic[word]

    return (notoccur_count / total) * 100


def map_test_into_unk(unigram_dic_train_with_unk, file, newfile):
    fr = open(file, 'r')
    fw = open(newfile, 'a')

    for line in fr:
        line = line.rstrip('\n')
        sp = line.split(' ')
        for word in sp:
            if word in unigram_dic_train_with_unk.keys():
                fw.write(word)
                fw.write(" ")
            else:
                fw.write('<unk> ')
                # print(word)
        fw.write("\n")


def calc_bigramtype_percent(biword_train_dict, biword_test_dic):
    notoccur_count = 0
    for biword in biword_test_dic:
        if biword in biword_train_dict.keys():
            continue
        else:
            notoccur_count += 1

    return (notoccur_count / len(biword_test_dic)) * 100


def calc_bigramtoken_percent(biword_train_dict, biword_test_dic):
    notoccur_count = 0
    total = 0
    for biword in biword_test_dic:
        if biword not in biword_train_dict.keys():
            notoccur_count += biword_test_dic[biword]

        total += biword_test_dic[biword]

    return (notoccur_count / total) * 100


def calc_unigram_model_logprob(file, trained_uni_prob_dic, unigram_dic_train_with_unk):
    probability = 0
    unigram_dic_line = unigramDictionary(file)
    unigram_dic_line.__delitem__('<s>')

    print("\nUnigram Model: ")

    fr = open(file, 'r')
    print("p( " + fr.readline().rstrip('\n') + " )")
    print('= ', end="")

    for word in unigram_dic_line:
        if word != '</s>':
            print('log (p(' + word + ')) + ', end="")
        else:
            print('log (p(' + word + '))')
            print('= ', end="")

    for word in unigram_dic_line:
        if word != '</s>':
            print('log ( ' + str(unigram_dic_train_with_unk[word]) + '/' + str(len(unigram_dic_train_with_unk)) + ' )  +  ', end="")
        else:
            print('log ( ' + str(unigram_dic_train_with_unk[word]) + '/' + str(len(unigram_dic_train_with_unk)) + ' )  +  ')
            print('= ', end="")

    for word in unigram_dic_line:
        if word in trained_uni_prob_dic.keys():
            n = trained_uni_prob_dic[word]
            log = math.log2(n) * unigram_dic_line[word]
            probability += log
            if word != '</s>':
                print(str(log) + ' + ', end="")
            else:
                print(log)
                print("= ", end="")
        else:
            if word != '</s>':
                print('0 + ', end="")
            else:
                print('0')
                print("= ", end="")

    print(probability)

    return probability


def calc_bi_logprob(file, unigram_dic, bigram_dic):

    bigram_dic_line = biDictionary(file)
    probability = 0

    print("\nBigram Model: ")
    fr = open(file, 'r')
    fr1 = open(file, 'r')
    print("p( " + fr.readline().rstrip('\n') + " )")
    print('= ', end="")

    for word in bigram_dic_line:
        if '</s>' not in word:
            print('log (p(' + word + ')) + ', end="")
        else:
            print('log (p(' + word + '))')
            print('= ', end="")

    for line in fr1:
        line = line.rstrip('\n')
        sp = line.split(' ')

        wc = 0
        prevword = ''
        biword = ''
        temp2 = ''

        for word in sp:
            wc += 1
            biword = biword + temp2 + word

            if wc == 1:
                prevword = word

            if wc == 2:
                wc = 1

                if biword in bigram_dic.keys():
                    prob = bigram_dic[biword] / unigram_dic[prevword]
                    log = math.log(prob, 2)
                    probability += log

                    if '</s>' not in word:
                        print('log ( ' + str(bigram_dic[biword]) + '/' + str(unigram_dic[prevword]) + ' )  ->  ', end="")
                        print(str(log) + ' + ', end="")
                    else:
                        print('log ( ' + str(bigram_dic[biword]) + '/' + str(unigram_dic[prevword]) + ' )  ->  ', end="")
                        print(log)
                        print('= ', end="")
                else:
                    if '</s>' not in word:
                        print('0 + ', end="")
                    else:
                        print('0')
                        print('= ', end="")

                temp2 = word
                prevword = word
                biword = ""

    print(probability)

    return probability


def calc_bi_smoothing_logprob(file, unigram_dic, bigram_dic):

    bigram_dic_line = biDictionary(file)
    probability = 0

    print("\nBigram Model With Add One Smoothing: ")
    fr = open(file, 'r')
    fr1 = open(file, 'r')
    print("p( " + fr.readline().rstrip('\n') + " )")
    print('= ', end="")

    for word in bigram_dic_line:
        if '</s>' not in word:
            print('log (p(' + word + ')) + ', end="")
        else:
            print('log (p(' + word + '))')
            print('= ', end="")

    for line in fr1:
        line = line.rstrip('\n')
        sp = line.split(' ')

        wc = 0
        prevword = ''
        biword = ''
        temp2 = ''

        for word in sp:
            wc += 1
            biword = biword + temp2 + word

            if wc == 1:
                prevword = word

            if wc == 2:
                wc = 1

                if biword in bigram_dic.keys():
                    prob = (bigram_dic[biword] + 1) / (unigram_dic[prevword] + len(unigram_dic))
                    log = math.log(prob, 2)
                    probability += log

                    if '</s>' not in word:
                        print('log ( ' + str(bigram_dic[biword]+1) + '/' + str(unigram_dic[prevword] + len(unigram_dic)) + ' )  ->  ', end="")
                        print(str(log) + ' + ', end="")
                    else:
                        print('log ( ' + str(bigram_dic[biword]+1) + '/' + str(unigram_dic[prevword] + len(unigram_dic)) + ' )  ->  ', end="")
                        print(log)
                        print('= ', end="")
                else:

                    prob = 1 / (unigram_dic[prevword] + len(unigram_dic))
                    log = math.log(prob, 2)
                    probability += log

                    if '</s>' not in word:
                        print('log ( ' + str(1) + '/' + str(unigram_dic[prevword] + len(unigram_dic)) + ' )  ->  ', end="")
                        print(str(log) + ' + ', end="")
                    else:
                        print('log ( ' + str(1) + '/' + str(unigram_dic[prevword] + len(unigram_dic)) + ' )  ->  ', end="")
                        print(log)
                        print('= ', end="")

                temp2 = word
                prevword = word
                biword = ""

    print(probability)

    return probability


def calc_perplexity_unigram(file, trained_uni_prob_dic):
    unigram_dic_train_with_unk = unigramDictionary("trainWithUnk.txt")
    unigram_dic_line = unigramDictionary(file)
    base = calc_unigram_model_logprob(file, trained_uni_prob_dic, unigram_dic_train_with_unk)
    base = base / totalUniWordtokens(unigram_dic_line)
    perplexity = math.pow(2, -base)
    return perplexity


def calc_perplexity_bigram(file, unigram_dic, bigram_dic):
    base = calc_bi_logprob(file, unigram_dic, bigram_dic)
    unigram_dic_line = unigramDictionary(file)
    base = base / totalUniWordtokens(unigram_dic_line)
    perplexity = math.pow(2, -base)
    return perplexity


def calc_perplexity_bigram_smoothing(file, unigram_dic, bigram_dic):
    base = calc_bi_smoothing_logprob(file, unigram_dic, bigram_dic)
    unigram_dic_line = unigramDictionary(file)
    base = base / totalUniWordtokens(unigram_dic_line)
    perplexity = math.pow(2, -base)
    return perplexity


def printDictionary(dictionary):
    fw = open("storebigrams", "a")
    for word in dictionary:
        print(word + " - " + str(dictionary[word]))


def question1():
    unigram_dictionary = unigramDictionary("trainWithUnk.txt")
    print("\nQuestion 1:")
    print(len(unigram_dictionary))
    print('\n')


def question2():
    unigram_dictionary = unigramDictionary("trainWithUnk.txt")
    print(unigram_dictionary)
    total_words_token = totalUniWordtokens(unigram_dictionary)
    print("\nQuestion 2:")
    print(total_words_token)
    print('\n')


def question3():
    uniword_dic_train = unigramDictionary("trainPad.txt")
    uniword_dic_test = unigramDictionary("testPad.txt")
    #printDictionary(uniword_dic_test)
    wordtype_percent = calc_wordtype_percent(uniword_dic_train, uniword_dic_test)
    wordtoken_percent = calc_wordtoken_percent(uniword_dic_train, uniword_dic_test)

    print("\nQuestion 3:")
    print('WordType Percentage in Test Data not in Train Data: ' + str(wordtype_percent))
    print('WordToken Percentage in Test Data not in Train Data: ' + str(wordtoken_percent))
    print('\n')

def question4():
    #uniword_dic_test = unigramDictionary("testPad.txt")
    #replaceWithUnk('trainPad.txt', 'trainWithUnk.txt')
    #unigram_dic_train_with_unk = unigramDictionary("trainWithUnk.txt")
    #map_test_into_unk(unigram_dic_train_with_unk, "testPad.txt", "testWithUnk.txt")

    bigram_dic_train = biDictionary("trainWithUnk.txt")
    bigram_dic_test = biDictionary("testWithUnk.txt")
    #printDictionary(bigram_dic_test)
    bigramtype_percent = calc_bigramtype_percent(bigram_dic_train, bigram_dic_test)
    bigramtoken_percent = calc_bigramtoken_percent(bigram_dic_train, bigram_dic_test)

    print("\nQuestion 4:")
    print('Bigram WordType Percentage in Test Data not in Train Data: ' + str(bigramtype_percent))
    print('Bigram WordToken Percentage in Test Data not in Train Data: ' + str(bigramtoken_percent))
    print('\n')


def question5():
    #padFile('sentence.txt', 'sentencePad.txt')
    print("\nQuestion 5:")
    unigram_dic_train_with_unk = unigramDictionary("trainWithUnk.txt")
    total_unigram_count = totalUniWordtokens(unigram_dic_train_with_unk)
    unigram_prob_train = unigramTrainModel(unigram_dic_train_with_unk, total_unigram_count)
    calc_unigram_model_logprob('sentencePad.txt', unigram_prob_train, unigram_dic_train_with_unk)
    print('\n')

    bigram_dic_train = biDictionary("trainWithUnk.txt")
    calc_bi_logprob('sentencePad.txt', unigram_dic_train_with_unk, bigram_dic_train)
    print('\n')

    calc_bi_smoothing_logprob('sentencePad.txt', unigram_dic_train_with_unk, bigram_dic_train)
    print('\n')


def question6():
    print("\nQuestion 6:\n")
    unigram_dic_train_with_unk = unigramDictionary("trainWithUnk.txt")
    total_unigram_count = totalUniWordtokens(unigram_dic_train_with_unk)
    unigram_prob_train = unigramTrainModel(unigram_dic_train_with_unk, total_unigram_count)
    perplexity_unigram = calc_perplexity_unigram("sentencePad.txt", unigram_prob_train)
    print("Perplexity under unigram model: " + str(perplexity_unigram))
    print('\n')

    bigram_dic_train = biDictionary("trainWithUnk.txt")
    perplexity_bigram = calc_perplexity_bigram("sentencePad.txt", unigram_dic_train_with_unk, bigram_dic_train)
    print("Perplexity under bigram model: " + str(perplexity_bigram))
    print('\n')

    perplexity_bigram_smoothing = calc_perplexity_bigram_smoothing("sentencePad.txt", unigram_dic_train_with_unk, bigram_dic_train)
    print("Perplexity under bigram-smoothing model: " + str(perplexity_bigram_smoothing))
    print('\n')


def question7():
    print("\nQuestion 7:\n")
    unigram_dic_train_with_unk = unigramDictionary("trainWithUnk.txt")
    total_unigram_count = totalUniWordtokens(unigram_dic_train_with_unk)
    unigram_prob_train = unigramTrainModel(unigram_dic_train_with_unk, total_unigram_count)
    perplexity_unigram = calc_perplexity_unigram("testWithUnk.txt", unigram_prob_train)
    print("Perplexity under unigram model: " + str(perplexity_unigram))
    print('\n')

    bigram_dic_train = biDictionary("trainWithUnk.txt")
    perplexity_bigram = calc_perplexity_bigram("testWithUnk.txt", unigram_dic_train_with_unk, bigram_dic_train)
    print("Perplexity under bigram model: " + str(perplexity_bigram))
    print('\n')

    perplexity_bigram_smoothing = calc_perplexity_bigram_smoothing("testWithUnk.txt", unigram_dic_train_with_unk,
                                                                   bigram_dic_train)
    print("Perplexity under bigram-smoothing model: " + str(perplexity_bigram_smoothing))
    print('\n')


def preprocess():
    padFile('train.txt', 'trainPad.txt')
    replaceWithUnk('trainPad.txt', 'trainWithUnk.txt')


def choosequestion():

    check = True
    while check:
        que = input("Enter question number (eg 1 for question_1): ")
        if que == '1':
            question1()
        elif que == '2':
            question2()
        elif que == '3':
            question3()
        elif que == '4':
            question4()
        elif que == '5':
            question5()
        elif que == '6':
            question6()
        elif que == '7':
            question7()
        else:
            print("Invalid Number!!")

        ask = input("Do you want to ask another question (y/n): ")
        if ask == "y" or ask == "Y":
            check = True
        else:
            check = False

#preprocess()
#question1()
#question2()
#question3()
#question4()
#question5()
#question6()
#question7()

choosequestion()





