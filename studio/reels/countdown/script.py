# Countdown reel script: each line is a list of caption chunks; each chunk is a
# list of (display word, phonemes, big?) — big words are the shouted keywords.
TITLE = "6 Data Structures You Need"
LINES = [
    # hook
    [[("Six", "sˈɪks", 1)],
     [("data", "dˈeɪɾə", 0), ("structures", "stɹˈʌktʃɚz", 1)],
     [("every", "ˈɛvɹi", 0), ("coder", "kˈoʊdɚ", 1), ("needs.", "nˈiːdz.", 0)],
     [("Don't", "dˈoʊnt", 0), ("skip", "skˈɪp", 1)],
     [("the", "ðə", 0), ("last", "lˈæst", 1), ("one!", "wˈʌn!", 0)]],
    # 1 array
    [[("One:", "wˈʌn:", 0), ("Array.", "ɐɹˈeɪ.", 1)],
     [("Items", "ˈaɪɾəmz", 0), ("in", "ɪn", 0), ("a", "ɐ", 0), ("row.", "ɹˈoʊ.", 1)],
     [("Grab", "ɡɹˈæb", 1), ("any", "ˈɛni", 0), ("one", "wˈʌn", 0)],
     [("by", "baɪ", 0), ("its", "ɪts", 0), ("number.", "nˈʌmbɚ.", 1)]],
    # 2 stack
    [[("Two:", "tˈuː:", 0), ("Stack.", "stˈæk.", 1)],
     [("Like", "lˈaɪk", 0), ("a", "ɐ", 0), ("pile", "pˈaɪl", 0), ("of", "ʌv", 0), ("plates.", "plˈeɪts.", 1)],
     [("Last", "lˈæst", 1), ("in,", "ˈɪn,", 0)],
     [("first", "fˈɜːst", 1), ("out.", "ˈaʊt.", 0)]],
    # 3 queue
    [[("Three:", "θɹˈiː:", 0), ("Queue.", "kjˈuː.", 1)],
     [("Like", "lˈaɪk", 0), ("a", "ɐ", 0), ("line", "lˈaɪn", 1)],
     [("for", "fɔːɹ", 0), ("chai.", "tʃˈaɪ.", 1)],
     [("First", "fˈɜːst", 1), ("in,", "ˈɪn,", 0)],
     [("first", "fˈɜːst", 1), ("out.", "ˈaʊt.", 0)]],
    # 4 hash map
    [[("Four:", "fˈoːɹ:", 0), ("Hash", "hˈæʃ", 1), ("map.", "mˈæp.", 1)],
     [("Give", "ɡˈɪv", 0), ("it", "ɪt", 0), ("a", "ɐ", 0), ("key,", "kˈiː,", 1)],
     [("get", "ɡˈɛt", 0), ("the", "ðə", 0), ("value.", "vˈæljuː.", 1)],
     [("Super", "sˈuːpɚ", 1), ("fast", "fˈæst", 0)],
     [("lookups.", "lˈʊkʌps.", 1)]],
    # 5 tree
    [[("Five:", "fˈaɪv:", 0), ("Tree.", "tɹˈiː.", 1)],
     [("One", "wˈʌn", 0), ("root,", "ɹˈuːt,", 1)],
     [("many", "mˈɛni", 0), ("branches.", "bɹˈæntʃᵻz.", 1)],
     [("Perfect", "pˈɜːfɛkt", 0), ("for", "fɔːɹ", 0), ("folders.", "fˈoʊldɚz.", 1)]],
    # 6 graph
    [[("Six:", "sˈɪks:", 0), ("Graph.", "ɡɹˈæf.", 1)],
     [("Dots", "dˈɑːts", 0), ("joined", "dʒˈɔɪnd", 1)],
     [("by", "baɪ", 0), ("lines.", "lˈaɪnz.", 1)],
     [("Maps", "mˈæps", 1)],
     [("and", "ænd", 0), ("friend", "fɹˈɛnd", 1), ("lists", "lˈɪsts", 0)],
     [("use", "jˈuːz", 0), ("these!", "ðˈiːz!", 1)]],
]

ITEMS = [  # name, number word, one-line description, summary tag, icon
    ("Array", "one", "Items in a row. Grab any one by its index.", "index", "array"),
    ("Stack", "two", "Like a pile of plates. Last in, first out.", "LIFO", "stack"),
    ("Queue", "three", "Like a line for chai. First in, first out.", "FIFO", "queue"),
    ("Hash map", "four", "Give it a key, get the value. Super fast.", "key → value", "hash"),
    ("Tree", "five", "One root, many branches. Think folders.", "hierarchy", "tree"),
    ("Graph", "six", "Dots joined by lines. Maps, friend lists.", "network", "graph"),
]
MOODS = ["curious", "working", "thinking", "study", "idea", "curious", "wow"]
