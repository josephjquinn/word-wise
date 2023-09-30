def badLetters(result, guess):
    """Finds incorrect letters in word"""
    bad_letters = []
    for i in range(0, 5):
        if result[i] == "w":
            bad_letters.append(guess[i])
    return bad_letters


def partialLetters(result, guess):
    """Finds correct letters that are misplaced in word"""
    partial_letters = []
    for i in range(0, 5):
        if result[i] == "y":
            partial_letters.append([guess[i], i])
    return partial_letters


def correctLetters(result, guess):
    """Finds fully correct letters in word"""
    correct_letters = []
    for i in range(0, 5):
        if result[i] == "g":
            correct_letters.append([guess[i], i])
    return correct_letters


def word_remover(result, guess, possible_words):
    """Returns the list of words with incorrect possibilties removed"""
    bad_letters = badLetters(result, guess)
    correct_letters = correctLetters(result, guess)
    partial_letters = partialLetters(result, guess)
    good_letters = []
    for g in correct_letters:
        good_letters.append(g[0])
    for p in partial_letters:
        good_letters.append(p[0])

    acceptable_words1 = []
    for w in possible_words:
        check = 0
        for b in bad_letters:
            if b in w:
                if b in good_letters:
                    pass
                else:
                    check = 1
                    break
        if check == 0:
            acceptable_words1.append(w)
    # print(acceptable_words1)

    acceptable_words2 = []
    for w in acceptable_words1:
        check = 0
        for g in correct_letters:
            if w[g[1]] != g[0]:
                check = 1
                break
        if check == 0:
            acceptable_words2.append(w)
    # print(acceptable_words2)

    acceptable_words3 = []
    for w in acceptable_words2:
        check = 0
        for p in partial_letters:
            if w[p[1]] == p[0]:
                check = 1
                break
        if check == 0:
            acceptable_words3.append(w)
    # print(acceptable_words3)

    acceptable_words4 = []
    for w in acceptable_words3:
        check = 0
        for g in good_letters:
            if g not in w:
                check = 1
                break
        if check == 0:
            acceptable_words4.append(w)
    # print(acceptable_words4)

    acceptable_words5 = []
    for w in acceptable_words4:
        check = 0
        for b in bad_letters:
            if b in good_letters:
                if w.count(b) != good_letters.count(b):
                    check = 1
                    break
        if check == 0:
            acceptable_words5.append(w)

    return acceptable_words5


def letterFreq(possible_words):
    """Finds frequencies of letters in each position"""
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    arr = {}
    for c in alphabet:
        freq = [0, 0, 0, 0, 0]
        for i in range(0, 5):
            for w in possible_words:
                if w[i] == c:
                    freq[i] += 1
        arr.update({c: freq})
    return arr


def wordScore(possible_words, frequencies):
    """Computes a score based off letter frequencies"""
    words = {}
    max_freq = [0, 0, 0, 0, 0]
    for c in frequencies:
        for i in range(0, 5):
            if max_freq[i] < frequencies[c][i]:
                max_freq[i] = frequencies[c][i]
    for w in possible_words:
        score = 1
        for i in range(0, 5):
            c = w[i]
            score *= 1 + (frequencies[c][i] - max_freq[i]) ** 2
        words.update({w: score})
        import numpy
        score += numpy.random.uniform(0,
                                      1)  # this will increase expectation from 2.95 to 3.23, but is technically fairer
    return words


def bestWord(possible_words, frequencies):
    """Finds the best word"""
    max_score = 1000000000000000000  # start with a ridiculous score
    best_word = "words"  # start with a random word
    scores = wordScore(possible_words, frequencies)
    for w in possible_words:
        if scores[w] < max_score:
            max_score = scores[w]
            best_word = w
    return best_word


