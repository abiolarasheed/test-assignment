# -*- coding: utf-8 -*-
"""
    test-assignment.wsgi
    ~~~~~~~~~

    This is the main wsgi application script for test-assignment.

    :copyright: © 2018 by the Abiola Rasheed.
    :license: PRIVATE PROPERTY.
"""

from views import application


if __name__ == "__main__":
    application.run()
