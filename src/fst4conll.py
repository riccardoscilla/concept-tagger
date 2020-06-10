def read_fst4conll(fst_file, fs="\t", oov='<unk>', otag='O', sep='+', split=False):
    """
    :param corpus_file: corpus in conll format
    :param fs: field separator
    :param oov: token to map to otag (we need to get rid of <unk> in labels)
    :param otag: otag symbol
    :param sep: 
    :param split:
    :return: corpus 
    """
    sents = []  # list to hold words list sequences
    words = []  # list to hold feature tuples

    for line in open(fst_file):
        line = line.strip()
        if len(line.strip()) > 0:
            feats = tuple(line.strip().split(fs))
            # arc has minimum 3 columns, else final state
            if len(feats) >= 3:
                ist = feats[2]  # 3rd column (input)
                ost = feats[3]  # 4th column (output)
                # replace '<unk>' with 'O'
                ost = otag if ost == oov else ost
                # ignore for now
                ost = ost.split(sep)[1] if split and ost != otag else ost
                
                words.append((ist, ost))
            else:
                sents.append(words)
                words = []
        else:
            if len(words) > 0:
                sents.append(words) 
                words = []
    return sents
