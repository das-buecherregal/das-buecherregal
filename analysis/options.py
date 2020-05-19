import re

groupedRules = {
    "Conjunctions": {
        'subordinating conjunctions': {
            "pattern": re.compile('(, (als ob|bevor|dass|daß|da|falls|nachdem|obwohl|ob|seitdem|seit|weil|wenn) )'),
            "description": "instances of the subordinating conjunctions: als ob, bevor, da, dass/daß, falls, nachdem, ob, obwohl, seit, seitdem, weil, or wenn"
        },
        'words used as preposition and subordinating conjunction': {
            "pattern": re.compile('(?<![a-zA-ZäöüßÄÖÜ])(während|seit)(?![a-zA-ZäöüßÄÖÜ])', re.IGNORECASE),
            "description": "instances of 'während' ('during' and 'while') and 'seit' ('since' and 'for')"
        },
        'tricky conjunctions': {
            "pattern": re.compile('(, (damit|indem))'),
            "description": "instances of the conjunctions 'damit' and 'indem'"
        },
        'als': {
            "pattern": re.compile('(als)', re.IGNORECASE),
            "description": "instances of 'als' in all of its uses (than, while, when, as, etc.)"
        }
    },
    "Relative Clauses": {
        'relative clause': {
            "pattern": re.compile('(, (die|das|der|den|dem|denen|dessen|deren) )'),
            "description": "relative clauses beginning with a relative pronoun"
        },
        'relative clause starting with preposition': {
            "pattern": re.compile('(, (an|auf|außer|ausser|aus|bei|durch|für|gegen|hinter|in|mit|nach|neben|ohne|über|um|unter|vor|von|zu|zwischen) (denen|deren|dessen|das|dem|den|der|die))'),
            "description": "relative clauses beginning with a preposition"
        },
        "relative clause starting with 'was'": {
            "pattern": re.compile('(?<![a-zA-ZäöüßÄÖÜ])((alles|das|etwas|nichts|wenig|viel), was)'),
            "description": "relative clause starting with 'was'"
        }
    },
    "Verbs": {
        'infinitive clause': {
            "pattern": re.compile('(, ((an)?statt |ohne |um |)[a-zA-ZäöüßÄÖÜ ]*zu {0,1}[a-zäöüß]{3,}(t|en))'),
            "description": "instances of anstatt, ohne, statt, um, or nothing ... zu (instead of, without, in order to)"
        },
        'passive tense': {
            "pattern": re.compile('(((werden|wird)|(wurd(en|e)))[a-zA-ZäöüßÄÖÜ ]* ge(([a-zäöüß]{2,}en)|([a-zäöüß]{3,}t)))(?![a-zA-ZäöüßÄÖÜ])'),
            "description": "instances of passive tense"
        },
        'modal verbs (dürfen, können, möchten, mögen, müssen, sollen, wollen)': {
            "pattern": re.compile('(?<![a-zA-ZäöüßÄÖÜ])(dürfen|darf|können|könnte|kann|möchten|möchte|mögen|mag|müssen|muss|muß|sollen|sollte|soll|wollte|wollen|will)'),
            "description": "modal verbs in first person, second person formal, or third person"
        },
        'modal verbs (conjugated in du/ihr form)': {
            "pattern": re.compile('(?<![a-zA-ZäöüßÄÖÜ])(darfst|kannst|könntest|möchtest|musst|mußt|sollst|willst)'),
            "description": "modal verbs in second person informal (singular or plural)"
        },
        "past participle + 'sein'": {
            "pattern": re.compile('(((bin|bist|ist|seid|sind)[a-zA-ZäöüßÄÖÜ]* (gekommen|gewesen|geflogen|gefahren|geblieben|geworden|geschwommen|auferstanden|aufgewacht|aufgestanden|geschehen|passiert))|((gekommen|gewesen|geflogen|gefahren|geblieben|geworden|geschwommen|auferstanden|aufgewacht|aufgestanden|geschehen|passiert) (bin|bist|ist|seid|sind)))'),
            "description": "instances of past participles that require 'sein'"
        },
        'simple/weak past participle': {
            "pattern": re.compile('(?<![a-zA-ZäöüßÄÖÜ])(ge([a-zäöüß]{3,}t))(?![a-zA-ZäöüßÄÖÜ])'),
            "description": "past participles beginning with ge- and ending in -t"
        },
        'irregular past participle': {
            "pattern": re.compile('(?<![a-zA-ZäöüßÄÖÜ])(ge([a-zäöüß]{2,}en))(?![a-zA-ZäöüßÄÖÜ])'),
            "description": "past participles beginning with ge- and ending in -en"
        },
        'inseparable prefix verbs': {
            "pattern": re.compile('((?<![a-zA-ZäöüßÄÖÜ])((be|emp|ent|er|miss|ver|zer)(?![a-zäöüß]*(heit|keit|lich|ung))[a-zäöüß]{5,}))'),
            "description": "verbs beginning with be-, emp-, ent-, er-, miss-, ver-, or zer-"
        },
        'inseparable prefix past participle': {
            "pattern": re.compile('(?<![a-zA-ZäöüßÄÖÜ])((be|emp|ent|er|miss|ver|zer)(?![a-zäöüß]*(heit|keit))[a-zäöüß]{3,}(t|en))(?![a-zA-ZäöüßÄÖÜ])'),
            "description": "past participles beginning with be-, emp-, ent-, er-, miss-, ver-, or zu-"
        },
        "'ge-' infinitive": {
            "pattern": re.compile('(gefallen|geschehen|gefiel|geschah|gewinnen|gewann)'),
            "description": "instances of infinitives beginning with ge-"
        },
        'lassen': {
            "pattern": re.compile('lassen|lässt|gelassen'),
            "description": "instances of 'lassen'"
        },
        "'sich' + lassen": {
            "pattern": re.compile('((sich [a-zA-ZäöüßÄÖÜ ]*(lassen|lässt|gelassen))|((lassen|lässt|gelassen)[a-zA-ZäöüßÄÖÜ ]* sich))'),
            "description": "instances of 'sich lassen'"
        }
    },
    "Prefixes/Suffixes/Compounds": {
        'da-compounds': {
            "pattern": re.compile('(?<![a-zA-ZäöüßÄÖÜ])(d(a?)(bei|für|mit|nach|ran|rauf|raus|rin|rum|runter|rüber|von|vor|zu))(?![a-zA-ZäöüßÄÖÜ])'),
            "description": "compounds such as dabei, daran, dazu, drunter, etc."
        },
        'suffixes': {
            "pattern": re.compile('([a-zäöüß]+(bar|fach|lich|los|mal))(?![a-zA-ZäöüßÄÖÜ])'),
            "description": "words ending in -bar, -fach, -lich, -los, or -mal"
        },
        'word families (-heit, -keit, -ung)': {
            "pattern": re.compile('(?<![a-zA-ZäöüßÄÖÜ])([A-ZÄÖÜ][a-zäöüß]+(keit|heit|ung))(?![a-zA-ZäöüßÄÖÜ])'),
            "description": "nouns ending in -keit, -heit, or -ung"
        }
    },
    "Miscellaneous": {
        'comparative': {
            "pattern": re.compile(r'\b(?!oder|welcher|daher|eher|immer|hier|aber)(?<![A-ZÄÖÜ])([a-zäöüß]{2,}er als)'),
            "description": "instances of comparisons usually with 'als', for example, 'größer als'"
        },
        'negation': {
            "pattern": re.compile('(nicht nur [a-zA-ZäöüßÄÖÜ ,]+ sondern)'),
            "description": "instances of 'nicht nur ... sondern' ('not only ... but also')"
        },
        'embedded adjectives': {
            "pattern": re.compile('((die|der|dem|den) (die|der|dem|den) )'),
            "description": "instances of embedded extended adjectives"
        },
        'selbst/selber': {
            "pattern": re.compile('(?<![a-zA-ZäöüßÄÖÜ])(selbst|selber)(?![a-zA-ZäöüßÄÖÜ])'),
            "description": "instances of 'selbst' or 'selber'"
        },
        "defining 'home'": {
            "pattern": re.compile('(((zu|nach) {0,1}(?i)(Hause))|daheim|Heimat)'),
            "description": "instances of nach Hause/zu Hause/nachhause/zuhause/daheim/Heimat"
        }
    }
}
