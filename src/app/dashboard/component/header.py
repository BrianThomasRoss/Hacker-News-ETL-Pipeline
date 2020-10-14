
# -*- coding: utf-8 -*-
"""
Application navigation bar.
Navbar docs: https://dash-bootstrap-components.opensource.faculty.ai/l/components/navbar
"""
import dash_html_components as html
import dash_bootstrap_components as dbc

content = html.Div(
    [
        dbc.NavbarSimple(
            brand="Election Sentiment 2020",
            brand_href="#",
            color="primary",
            dark=True,
        )
    ]
)