# -*- coding: utf-8 -*-
from exceptions import LexicallyWordException


class Word():
    """
    Word for conlangs

    Attributes:
        parent: [Word, ...]
            Where the word is derived from
        pos: str
            Part of speech
            Noun or Verb
        meaning: str
            The meaning of the word
        ipa: unicode str
            How its said
        notes: str, default=''
            Additional notes
    """
    def __init__(self, parent, pos, meaning, ipa, notes=''):
        self.parent = parent
        self.pos = pos
        self.meaning = meaning
        self.ipa = ipa
        self.notes = notes

    def get(self, attribute):
        """Get the specific attribute (safe)"""
        attribute = attribute.lower()
        return {
            'parent': self.parent,
            'pos': self.pos,
            'meaning': self.meaning,
            'ipa': self.ipa,
            'notes': self.notes,
            'default': None
        }.get(attribute, 'default')

    def get_attr(self):
        """Get all Attributes"""
        return {
            'parent': self.parent,
            'pos': self.pos,
            'meaning': self.meaning,
            'ipa': self.ipa,
            'notes': self.notes
        }

    def __lt__(self, other):
        return self.ipa < other.ipa

    def __gt__(self, other):
        return self.ipa > other.ipa

    def __repr__(self):
        return 'lexically.word.Word({}, {}, {}, {}, notes={})'.format(
            repr(self.parent),
            repr(self.pos),
            repr(self.meaning),
            repr(self.ipa),
            repr(self.notes)
        )


def main():
    water = Word(['base'], 'Noun', 'Water', u'mɪ')
    add = Word(['base'], 'Verb', 'Add', u'və')
    for attribute in ['parent', 'pos', 'meaning', 'ipa', 'notes']:
        print(water.get(attribute))
        print(add.get(attribute))

if __name__ == '__main__':
    main()
