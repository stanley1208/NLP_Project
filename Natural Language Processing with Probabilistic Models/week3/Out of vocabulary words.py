from collections import Counter


def add_k_smoothing_probability(k,vocabulary_size,n_gram_count,n_gram_prefix_count):
    numerator=n_gram_count+k
    denominator=n_gram_prefix_count+k*vocabulary_size
    return numerator/denominator


# the target size of the vocabulary
M=3

# pre-calculated word counts
# Counter could be used to build this dictionary from the source corpus
word_counts={'happy':5,'because':3,'i':2,'am':2,'learning':3,',':1}
vocabulary=Counter(word_counts).most_common(M)

# remove the frequencies and leave just the words
vocabulary=[w[0] for w in vocabulary]

print(f'the new vocabulary containing {M} most frequent words: {vocabulary}')


# test if words in the input sentences are in the vocabulary, if OOV, print <UNK>
sentence=['am','i','learning']
output_sentence=[]
print(f'input sentence: {sentence}')

for w in sentence:
    if w in vocabulary:
        output_sentence.append(w)
    else:
        output_sentence.append('UNK')

print(f'output_sentence: {output_sentence}')


# iterate through all word counts and print words with given frequency f
f=3

for word,freq in word_counts.items():
    if freq==f:
        print(word)


# many <unk> low perplexity
training_set=['i','am','happy','because','i','am','learning','.']
training_set_unk=['i','am','<UNK>','<UNK>','i','am','<UNK>','<UNK>']

test_set=['i','am','learning']
test_set_unk=['i','am','<UNK>']

M=len(test_set)
probability=1
probability_unk=1

# pre-calculated probabilities
bigram_probabilities={('i','am'):1.0,('am','happy'):0.5,('happy','because'):1.0,('because','i'):1.0,('am','learning'):0.5,('learning','.'):1.0}
bigram_probabilities_unk={('i','am'):1.0,('am','<UNK>'):1.0,('<UNK>','<UNK>'):0.5,('<UNK>','i'):0.25}


# got through the test set and calculate its bigram probability
for i in range(len(test_set)-1):
    bigram=tuple(test_set[i:i+2])
    probability=probability*bigram_probabilities[bigram]
    bigram_unk=tuple(test_set_unk[i:i+2])
    probability_unk=probability_unk*bigram_probabilities_unk[bigram_unk]

# calculate perplexity for both original test set and test set with <UNK>
perplexity=probability**(-1/M)
perplexity_unk=probability_unk**(-1/M)

print(f'perplexity for the training set:{perplexity}')
print(f'perplexity for the training set with <UNK>:{perplexity_unk}')


trigram_probabilities={('i','am','happy'):2}
bigram_probabilities={('am','happy'):10}
vocabulary_size=5
k=1


probability_known_trigram=add_k_smoothing_probability(k,
                                                      vocabulary_size,
                                                      trigram_probabilities[('i','am','happy')],
                                                      bigram_probabilities[('am','happy')])

probability_unknown_trigram=add_k_smoothing_probability(k,
                                                        vocabulary_size,
                                                        0,
                                                        0)

print(f'probability_known_trigram: {probability_known_trigram}')
print(f'probability_unknown_trigram: {probability_unknown_trigram}')


# pre-calculated probabilities of all types of n-grams
trigram_probabilities={('i','am','happy'):0}
bigram_probabilities={('am','happy'):0.3}
unigram_probabilities={('happy'):0.4}

# this is the input trigram we need to estimate
trigram=('are','you','sad')

# find the last bigram and unigram of the input
bigram=trigram[1:3]
unigram=trigram[2]
print(f'besides the trigram {trigram} we also use bigram {bigram} and unigram {unigram}')

# 0.4 is used as an example, experimentally found for web-scale corpuses when using the "stupid" back-off
lambda_factor=0.4
probability_hat_trigram=0

# search for first non-zero probability starting with trigram
# to generalize this for any order of n-gram hierarchy,
# you could loop through the probability dictionaries instead of if/else cascade
if trigram not in trigram_probabilities or trigram_probabilities[trigram]==0:
    print(f'probability for trigram {trigram} not found')

    if bigram not in bigram_probabilities or bigram_probabilities[bigram]==0:
        print(f'probability for bigram {bigram} not found')

        if unigram in unigram_probabilities:
            print(f'probability for unigram {unigram} found\n')
            probability_hat_trigram=lambda_factor*lambda_factor*unigram_probabilities[unigram]
        else:
            probability_hat_trigram=0

    else:
        probability_hat_trigram=lambda_factor*bigram_probabilities[bigram]
else:
    probability_hat_trigram=trigram_probabilities[trigram]

print(f'probability for trigram {trigram} estimated as {probability_hat_trigram}')


# pre-calculated probabilities of all types of n-grams
trigram_probabilities={('i','am','happy'):0.155}
bigram_probabilities={('am','happy'):0.3}
unigram_probabilities={('happy'):0.4}


# the weights come from optimization on a validation set
lambda1=0.8
lambda2=0.4
lambda3=0.001

# this is the input trigram we need to estimate
trigram=('i','am','happy')

# find the last bigram and unigram of the input
bigram=trigram[1:3]
unigram=trigram[2]
print(f'besides the trigram {trigram} we also use bigram {bigram} and unigram {unigram}')


# in the production code, you would need to check if the probability n-gram dictionary contains the n-gram
probability_hat_trigram=lambda1*trigram_probabilities[trigram]+ lambda2*bigram_probabilities[bigram] + lambda3*unigram_probabilities[unigram]

print(f'probability for trigram {trigram} estimated as {probability_hat_trigram}')
