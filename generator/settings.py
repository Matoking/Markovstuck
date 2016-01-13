from markovstuck import settings

# Fetch data from these URLs
URLS = [
    "http://mspaintadventures.com/?search=6_1",  # Acts 1-4
    "http://mspaintadventures.com/?search=6_2",  # Act 5
    "http://mspaintadventures.com/?search=6_3",  # Act 6
]

# Names used in dialog logs
NAMES = [
    'GAMZEE', 'ROSESPRITE', 'DAVEPETASPRITE^2', 'FEFERI', 'VRISKA', 'FEFETASPRITE', 'ARADIABOT',
    'KARKAT', 'JAKE', 'JADE', 'JASPERSPRITE', 'TAVRISPRITE', 'ARANEA', 'MOTHERSPRITE', 'NANNASPRITEx2',
    'JADESPRITE', 'ROSE', 'CALLIOPE', 'NANNASPRITE', 'ERISOLSPRITE', 'ARADIASPRITE', 'DRAGONSPRITE', 'DAVE',
    'SOLLUX', 'NEPETASPRITE', 'TEREZI', 'EQUIUSPRITE', 'TAVROSPRITE', 'GG', 'GC', 'GA', 'GT', 'CG', 'FCG',
    'PCG', 'CC', 'CA', 'CT', 'AG', 'AC', 'AA', 'AT', 'TG', 'TC', 'TA', 'TT', 'UU', 'uu', 'JOHN', 'EB', 'ROXY',
    'ARQUIUSPRITE', 'MEENAH', 'JASPROSESPRITE^2', 'PCG', 'pipefan413', 'DIRK', 'JANE', 'FCG', 'DAVESPRITE', '?GG', 'CGA',
    'KANAYA', 'TAVROS', 'FCG2', 'PAT', 'CCT', 'fedorafreak', 'CCG', 'FAG', 'PAG', 'CAG', 'GCATAVROSPRITE', 'FTC', 'PTC',
    'PCC', 'CCC', 'ARADIA', 'FAA', 'CAA', 'PAA', '?CG', 'PCG2', 'PCG3', 'PCG4', 'PCG5', 'PCG6', 'PCG7', 'PCG8', '?TG',
    'CTG', 'CTA', 'PTA', 'NEPETA', 'FAC', 'CAC', 'FGC', 'PGC', 'CGC', 'EQUIUS', 'FCT', 'FGA', 'KANAYA?', 'ERIDAN', 'FCA',
    'PCA', 'CEB', ')(IC',
]

NAME_ALIASES = [
    ["GAMZEE", "TC", "FTC", "PTC"],
    ["ROSE", "TT", "ROSESPRITE"],
    ["FEFERI", "PCC", "CC", "CCC"],
    ["VRISKA", "AG", "CAG", "FAG", "PAG"],
    ["ARADIA", "ARADIABOT", "ARADIASPRITE", "FAA", "CAA", "AA", "PAA"],
    ["KARKAT", "CG", "CCG", "FCG", "PCG", "FCG2", "?CG",
        "PCG2", "PCG3", "PCG4", "PCG5", "PCG6", "PCG7", "PCG8"],
    ["JAKE", "GT"],
    ["JADE", "GG"],
    ["NANNASPRITE", "NANNASPRITEx2"],
    ["CALLIOPE", "UU"],
    ["DAVE", "TG", "?TG", "CTG"],
    ["SOLLUX", "CTA", "TA", "PTA"],
    ["NEPETA", "FAC", "AC", "CAC"],
    ["TEREZI", "GC", "FGC", "PGC", "CGC"],
    ["EQUIUS", "FCT", "CT"],
    ["TAVROS", "TAVROSPRITE", "AT"],
    ["KANAYA", "GA", "FGA", "KANAYA?"],
    ["ERIDAN", "CA", "FCA", "PCA"],
    ["JOHN", "EB", "CEB"],
    [")(IC"]
]

NAME_COLORS = {
    "GAMZEE": "#2b0057",
    "TC": "#2b0057",
    "FTC": "#2b0057",
    "PTC": "#2b0057",

    "ROSE": "#b536da",
    "TT": "#b536da",
    "ROSESPRITE": "#b536da",

    "DAVEPETASPRITE^2": ["#4ac925", "#f2a400"],

    "FEFERI": "#77003c",
    "CC": "#77003c",
    "PCC": "#77003c",
    "CCC": "#77003c",

    "VRISKA": "#005682",
    "AG": "#005682",
    "CAG": "#005682",
    "PAG": "#005682",
    "FAG": "#005682",

    "FEFETASPRITE": "#b536da",

    "ARADIA": "#a10000",
    "ARADIABOT": "#a10000",
    "ARADIASPRITE": "#a10000",
    "AA": "#a10000",
    "CAA": "#a10000",
    "FAA": "#a10000",
    "PAA": "#a10000",

    "KARKAT": "#626262",
    "CG": "#626262",
    "CCG": "#626262",
    "FCG": "#626262",
    "FCG2": "#626262",
    "PCG": "#626262",
    "PCG2": "#626262",
    "PCG3": "#626262",
    "PCG4": "#626262",
    "PCG5": "#626262",
    "PCG6": "#626262",
    "PCG7": "#626262",
    "PCG8": "#626262",
    "?CG": "#626262",

    "JAKE": "#1f9400",
    "GT": "#1f9400",

    "JADE": "#4ac925",
    "GG": "#4ac925",
    "?GG": "#4ac925",

    "JASPERSPRITE": "#f141ef",

    "TAVRISPRITE": "#0715cd",

    "ARANEA": "#005682",

    "NANNASPRITE": "#00d5f2",
    "NANNASPRITEx2": "#00d5f2",

    "JADESPRITE": "#1f9400",

    "CALLIOPE": "#929292",
    "UU": "#929292",

    "ERISOLSPRITE": "#4ac925",

    "DAVE": "#e00707",
    "TG": "#e00707",
    "CTG": "#e00707",
    "?TG": "#e00707",

    "SOLLUX": "#a1a100",
    "TA": "#a1a100",
    "PTA": "#a1a100",
    "CTA": "#a1a100",

    "NEPETA": "#416600",
    "NEPETASPRITE": "#416600",
    "AC": "#416600",
    "CAC": "#416600",
    "FAC": "#416600",

    "TEREZI": "#008282",
    "GC": "#008282",
    "FGC": "#008282",
    "PGC": "#008282",
    "CGC": "#008282",

    "EQUIUS": "#000056",
    "EQUIUSPRITE": "#000056",
    "FCT": "#000056",
    "CT": "#000056",
    "CCT": "#000056",

    "TAVROS": "#a15000",
    "TAVROSPRITE": "#a15000",
    "AT": "#a15000",
    "PAT": "#a15000",

    "ROXY": "#ff6ff2",

    "ARQUIUSPRITE": "#e00707",

    "MEENAH": "#77003c",

    "JASPROSESPRITE^2": "#b536da",

    "pipefan413": "#4b4b4b",

    "DIRK": "#f2a400",

    "JANE": "#00d5f2",

    "DAVESPRITE": "#f2a400",

    "KANAYA": "#008141",
    "KANAYA?": "#008141",
    "GA": "#008141",
    "CGA": "#008141",
    "FGA": "#008141",

    "fedorafreak": "#4b4b4b",

    "JOHN": "#0715cd",
    "EB": "#0715cd",
    "CEB": "#0715cd",

    "ERIDAN": "#6a006a",
    "CA": "#6a006a",
    "FCA": "#6a006a",
    "PCA": "#6a006a",

    "GCATAVROSPRITE": "#0715cd",

    ")(IC": "#77003c",

    "uu": "#323232",
}

# The images are downloaded from the URL http://cdn.mspaintadventures.com/storyfiles/hs2/XXXXX.gif
# starting from IMAGE_START to IMAGE_END
IMAGE_START = 1
IMAGE_END = 7932

# Where to save the loaded images
IMAGE_PATH = "%s/img/hs2" % settings.STATICFILES_DIRS[0]
