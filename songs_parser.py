import os
import sys
import h5py
import json

# Creates a JSON for artist_id : artist_name
def create_artists_list(walk_dir, outfile):
    artists_list = {}
    #c = 0
    for root, subdirs, files in os.walk(walk_dir):
        for filename in files:
            if ".h5" in filename:
                file_path = os.path.join(root, filename)
                #print('Processing file {}'.format(filename))
                with h5py.File(file_path, 'r') as f:
                    artist_id = list(f['metadata']['songs']['artist_id'])[0].decode()
                    artist_name = list(f['metadata']['songs']['artist_name'])[0].decode()
                    artists_list[artist_id] = artist_name
                    #c = c + 1
                    #if c%100 == 0:
                        #print(c)
                    #print("{}: {}".format(artist_id,artist_name))

    with open(outfile, 'w') as f:
        json.dump(artists_list, f)

# Creates a JSON for artist_id : [similar_artist_ids]
def create_similar_artists_dict(walk_dir, outfile):
    similar_list = {}
    #c = 0
    for root, subdirs, files in os.walk(walk_dir):
        for filename in files:
            if ".h5" in filename:
                file_path = os.path.join(root, filename)
                #print('Processing file {}'.format(filename))
                with h5py.File(file_path, 'r') as f:
                    artist_id = list(f['metadata']['songs']['artist_id'])[0].decode()
                    similar_artists = list(f['metadata']['similar_artists'])
                    similar_decoded = [x.decode() for x in similar_artists]
                    similar_list[artist_id] = similar_decoded
                    #c = c + 1
                    #if c%100 == 0:
                        #print(c)

    with open(outfile, 'w') as f:
        json.dump(similar_list, f)

# Creates clusters based on similar artists
def cluster_artists(similar_list, outfile):
    current_cluster = -1
    clusters = {}
    reverse_clusters = {}
    with open(similar_list, 'r') as f:
        sim = json.load(f)
    for artist in sim:
        if artist not in clusters:
            current_cluster = current_cluster + 1
            clusters[artist] = current_cluster
        for x in sim[artist]:
            if x in sim and x not in clusters:
                clusters[x] = clusters[artist]

    for n in range(current_cluster):
        reverse_clusters[n] = [k for k,v in clusters.items() if v == n]

    with open(outfile, 'w') as f:
        json.dump(reverse_clusters, f)



#create_artists_list(sys.argv[1], "artists_list.txt")
#create_similar_artists_dict(sys.argv[1], "artists_similar.txt")
cluster_artists("artists_similar.txt", "clusters.txt")
