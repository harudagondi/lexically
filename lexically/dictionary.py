# -*- coding: utf-8 -*-
import json
from jinja2 import Template
from word import Word
from exceptions import LexicallyDictionaryException


class Dictionary():
    """
    Containers for class Word

    Attributes:
        dictionary: [Word]
            Contains the Words
        language: str
            The name of the language
    """
    def __init__(self, language='Gamerenye'):
        self.dictionary = []
        self.language = language

    def add_word(self, word):
        """Add a word to the dictionary"""
        if word.ipa in [word.ipa for word in self.dictionary]:
            raise LexicallyDictionaryException('Word entered already exists')
        self.dictionary.append(word)
        return self

    def del_word(self, ipa):
        for word in self.dictionary:
            if word.ipa == ipa:
                self.dictionary.remove(word)
                return word
        else:
            return None

    def sort(self):
        """Sort the dictionary by its IPA"""
        self.dictionary.sort()

    def _save_as_json(self):
        """Saves the Dictionary to a .json file"""
        words = {}
        for word in self.dictionary:
            words[word.ipa] = {
                'parent': word.parent,
                'pos': word.pos,
                'meaning': word.meaning,
                'notes': word.notes
            }
        return words

    def save_file(self, filename='dictionary'):
        with open('{}.json'.format(filename), 'w', encoding='utf-8') as f:
            json.dump(self._save_as_json(), f, indent=4)
        return json.dumps(self._save_as_json())

    def save(self):
        return json.dumps(self._save_as_json(), indent=4)

    def load(self, filename='dictionary'):
        """Load the .json file"""
        words = []
        with open('{}.json'.format(filename), 'r') as f:
            json_dump = json.load(f)
        for item in json_dump:
            words.append(Word(
                json_dump[item]['parent'],
                json_dump[item]['pos'],
                json_dump[item]['meaning'],
                item,
                notes=json_dump[item]['notes']
            ))
        self.dictionary = words
        return self.dictionary

    def export_as_html(self, filename="dictionary"):
        """
        Exports the dictionary as an .html file

        Arguments:
            language: str
                The name of the language
            filename: str, default='dictionary'
                The file name

        Returns:
            The rendered jinja2.Template
        """
        skeleton = Template("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Dictionary of {{ language }}</title>
            <meta charset="UTF-8">
            <style>
                td, th {
                    border: 1px solid #333;
                    padding: 0.5rem;
                }
                td:first-child {
                    max-width: 5em;
                }
                body {
                    font-family: monofur, monospace;
                }
            </style>
        </head>
        <body>
            <table>
                <thead>
                    <tr>
                        <th>Parent(s)</th>
                        <th>Part of Speech</th>
                        <th>Meaning</th>
                        <th>IPA</th>
                        <th>Notes</th>
                    </tr>
                </thead>
                <tbody>
                    {{ content|safe }}
                </tbody>
            </table>
        </body>
        </html>
        """)
        template = Template("""
        <tr>
            <td>{{ parent }}</td>
            <td>{{ pos }}</td>
            <td>{{ meaning }}</td>
            <td>{{ ipa }}</td>
            <td>{{ notes }}</td>
        </tr>
        """)
        htmlified_words = u''
        for word in self.dictionary:
            htmlified_words += template.render(
                parent=word.parent,
                pos=word.pos,
                meaning=word.meaning,
                ipa=word.ipa,
                notes=word.notes
            )
        with open('{}.html'.format(filename), 'w', encoding='utf-8') as f:
            f.write(skeleton.render(
                language=self.language,
                content=htmlified_words
            ))
        return skeleton.render(
            language=self.language,
            content=htmlified_words
        )

    def __repr__(self):
        result = 'lexically.dictionary.Dictionary()'
        for word in self.dictionary:
            result += '.add_word({})'.format(repr(word))
        return result

    def to_dict(self):
        words = []
        for word in self.dictionary:
            words.append(word.get_attr())
        return words


def main():
    water = Word(['base'], 'Noun', 'Water', u'mɪ')
    fruit = Word(['base'], 'Noun', 'Fruit', u'd͡ʒæɹæ')
    water_fruit = Word([u'mɪ', u'd͡ʒæɹæ'],
                       'Noun',
                       'A fruit native to WaterLand',
                       u'mɪd͡ʒæɹæ')
    add = Word(['base'], 'Verb', 'Add', u'və')
    d = Dictionary()
    d.add_word(water).add_word(add).add_word(fruit).add_word(water_fruit)
    print(d.save_file())
    d.sort()
    d.export_as_html(u'Gamerenye')

if __name__ == '__main__':
    main()
