from collections import namedtuple

clusters = {}

with open('data/clusters.txt', 'r') as clust:
    clust_to_word = {}
    for line in clust:
        line = line.split()
        ID = line[0]
        word = line[1]
        if ID in clust_to_word:
            clust_to_word[ID].append(word)
        else:
            clust_to_word[ID] = [word]

    Cluster = namedtuple('Cluster', ['id', 'words'])
    id_to_clust = {}
    for ID, words in clust_to_word.iteritems():
        for word in words:
            if ID in id_to_clust:
                id_to_clust[ID].words.append(word)
                clusters[word] = id_to_clust[ID]
            else:
                id_to_clust[ID] = Cluster(ID, [word])
                clusters[word] = id_to_clust[ID]


def shares_cluster(w1, w2):
    if w1 in clusters and w2 in clusters:
        return clusters[w1].id == clusters[w2].id
    else:
        return w1 == w2

def get_cluster_id(word):
    if word in clusters:
        return clusters[word].id
    else:
        # If a word does not exist in our clusters, we return the word as its own ID
        return bin(hash(word))[2:]

def get_cluster(word):
    if word in clusters:
        return clusters[word].words
    else:
        return [word]


if __name__ == '__main__':
    while True:
        x = raw_input()
        print "ID: " + get_cluster_id(x)
        print "CLUSTER: " + str(get_cluster(x))
