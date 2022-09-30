import re
import os

import yaml
import jinja2

REGIONS_TO_DISPLAY = ['EU', 'US', 'europe-west1', 'your-region2']
REPO = 'https://github.com/unytics/bigfunctions'


INDEX_PAGE_TEMPLATE= jinja2.Template('''---
hide:
  - navigation
---

## 📄 Overview

!!! note ""

    BigFunctions are public BigQuery routines that give you **super-SQL-powers** in BigQuery 💪.


    {% for category, category_conf in categories.items() %}

    **{{ category_conf.emoticon }} {{ category|title }}**

    {% for name, conf in category_conf.bigfunctions.items() -%}
    {% set bigfunction_description_lines = conf.description.split('\n') %}
    - [<code>{{ name }}({% for argument in conf.arguments %}{{ argument.name | replace('{{region}}', region) }}{% if not loop.last %}, {% endif %}{% endfor %})</code>](#{{ name }}): {{ bigfunction_description_lines[0] }}
    {% endfor %}

    {% endfor %}

    **🔴 Before using see --> [Getting Started](/bigfunctions/getting_started/)**


''')



CATEGORY_PAGE_HEADER_TEMPLATE = jinja2.Template('''
<div style="margin-top: 6rem;"></div>


## {{ category_emoticon }} {{ category|title }}

!!! note ""
    **{{ category_title }} **

    {{ category_subtitle }}

''')


CATEGORIES = {
    'explore': {
        'emoticon': '👀',
        'title': 'Explore data within BigQuery console',
        'subtitle': 'Make computations on BigQuery and display the results as data-vizualizations directly in BigQuery console.',
        'bigfunctions': {
            f.replace('.yaml', ''): yaml.safe_load(open(f'bigfunctions/{f}', encoding='utf-8').read())
            for f in sorted([f for f in os.listdir('bigfunctions') if f.startswith('explore_')])
        },
    },
    'transform text': {
        'emoticon': '✨',
        'title': 'Transform data creatively',
        'subtitle': 'Be amazed with your new SQL powers.',
        'bigfunctions': {
            f.replace('.yaml', ''): yaml.safe_load(open(f'bigfunctions/{f}', encoding='utf-8').read())
            for f in sorted([f for f in os.listdir('bigfunctions') if f.startswith('transform_')])
        },
    },
    'notify': {
        'emoticon': '💬',
        'title': 'Send infos to your customers, alert the operations teams, send reportings to business',
        'subtitle': 'Spread the word to the world!',
        'bigfunctions': {
            f.replace('.yaml', ''): yaml.safe_load(open(f'bigfunctions/{f}', encoding='utf-8').read())
            for f in sorted([f for f in os.listdir('bigfunctions') if f.startswith('notify_')])
        },
    },
    'export': {
        'emoticon': '🚀',
        'title': 'Get the data out to the outside world',
        'subtitle': 'Make BigQuery as the golden source of all your SAAS and for all your usages',
        'bigfunctions': {
            f.replace('.yaml', ''): yaml.safe_load(open(f'bigfunctions/{f}', encoding='utf-8').read())
            for f in sorted([f for f in os.listdir('bigfunctions') if f.startswith('export_')])
        },
    },
    'utils': {
        'emoticon': '🔨',
        'title': '"Utils" BigFunctions',
        'subtitle': '',
        'bigfunctions': {
            f.replace('.yaml', ''): yaml.safe_load(open(f'bigfunctions/{f}', encoding='utf-8').read())
            for f in sorted([f for f in os.listdir('bigfunctions') if not any(f.startswith(prefix) for prefix in ['explore_', 'transform_', 'notify_', 'export_'])])
        },
    },
}


def generate_bigfunctions_index_page():
    output_filename = f'site/content/reference.md'
    content = INDEX_PAGE_TEMPLATE.render(categories=CATEGORIES)
    with open(output_filename, 'w', encoding='utf-8') as out:
        out.write(content)


def generate_bigfunctions_category_page(category, category_emoticon, category_title, category_subtitle, bigfunctions):
    output_filename = f'site/content/reference/{category}.md'
    documentations = []
    for name, conf in bigfunctions.items():
        if not conf or not isinstance(conf, dict):
            continue
        conf['name'] = name
        template = f'scripts/templates/doc_bigfunction.md'
        documentation = jinja2.Template(open(template, encoding='utf-8').read()).render(
            regions=REGIONS_TO_DISPLAY,
            repo=REPO,
            **conf,
        )
        documentations.append(documentation)


    header = CATEGORY_PAGE_HEADER_TEMPLATE.render(category=category, category_emoticon=category_emoticon, category_title=category_title, category_subtitle=category_subtitle)
    with open('site/content/reference.md', 'a', encoding='utf-8') as out:
        out.write(header)
        out.write('\n\n\n'.join(documentations))


if __name__ == '__main__':
    generate_bigfunctions_index_page()
    for category, category_conf in CATEGORIES.items():
        generate_bigfunctions_category_page(category, category_conf['emoticon'], category_conf['title'], category_conf['subtitle'], category_conf['bigfunctions'])
