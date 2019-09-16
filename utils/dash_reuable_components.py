import dash_core_components as dcc
import dash_html_components as html

# Display utility functions
def _merge(a, b):
    return dict(a, **b)

def _omit(omitted_keys, d):
    return {k: v for k, v in d.items() if k not in omitted_keys}

# Custom Display Components
def Card(children, **kwargs):
    return html.Section(
        children,
        style=_merge({
            'padding': 20,
            'margin': 5,
            'borderRadius': 5,
            'border': 'thin lightgrey solid',

            # To-Do: 改善の余地あり
            'user-select': 'none',
            '-moz-user-select': 'none',
            '-webkit-user-select': 'none',
            '-ms-user-select': 'none'
        }, kwargs.get('style', {})),
        **_omit(['style'], kwargs)
    )

def NamedDropdown(name, **kwargs):
    return html.Div(
        style={'margin': '10px 0px'},
        children=[
            html.P(
                children=f'{name}:',
                style={'margin-left': '3px'}
            ),

            dcc.Dropdown(**kwargs)
        ]
    )