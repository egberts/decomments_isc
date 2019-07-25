#!/usr/bin/env python3

##############################################################################

import os


def isc_comments_blanker(textdata):
    state_csc = False
    state_csc2 = False
    state_csc3 = False
    state_cxxsc = False
    state_cxxsc2 = False
    state_ssc = False
    newdata = ''
    for i in textdata:
        if not state_csc and not state_cxxsc and not state_ssc and not state_csc2 and not state_csc3 and not state_cxxsc2:
            # greenfield
            if i == '/':
                state_csc = True
                state_cxxsc = True
                # might need to backtrack and erase a char, later.
                newdata = newdata + i
            elif i == '#':
                state_ssc = True
                newdata = newdata + ' '
            else:
                newdata = newdata + i
        elif state_csc or state_cxxsc:
            if i == '/':
                # state transition
                state_csc = False
                state_cxxsc = False
                state_cxxsc2 = True
                newdata = newdata + ' '
            elif i == '*':
                state_csc = False
                state_cxxsc = False
                state_csc2 = True
                newdata = newdata + ' '
            else:
                newdata = newdata + i
                state_csc = False
                state_cxxsc = False

        elif state_csc2:
            if i == '*':
                state_csc2 = False
                state_csc3 = True
                # still eating comments
            # eat comment
            newdata = newdata + ' '
        elif state_csc3:
            if i == '/':
                # Stop eating comments
                state_csc = False
                state_csc2 = False
                state_csc3 = False
                state_cxxsc = False
                state_cxxsc2 = False
                state_ssc = False
            newdata = newdata + ' '
        elif state_cxxsc2 or state_ssc:
            # EOL kills these states
            if i == '\n':
                newdata = newdata + i
                # Stop eating comments
                state_csc = False
                state_csc2 = False
                state_csc3 = False
                state_cxxsc = False
                state_cxxsc2 = False
                state_ssc = False
            else:
                newdata = newdata + ' '
            # eat comment
        else:
            state_csc = False
            state_csc2 = False
            state_csc3 = False
            state_cxxsc = False
            state_cxxsc2 = False
            state_ssc = False
            newdata = newdata + i
    return newdata


if __name__ == "__main__":
    # Creating parser from parser model.
    #     parser = ParserPython(iscFile, debug=debug)

    testdata=""
    if False:
        # Load test JSON file
        current_dir = os.path.dirname(__file__)
        testdata = open(os.path.join(current_dir, '../test/test.isc')).read()

        print("testdata: ", testdata)

        testdata = isc_comments_blanker(testdata)

    test1 = """
    include a-b/c/d/e/f/g.conf;
    """
    test1s = isc_comments_blanker(test1)

    print("result: ", testdata)

    exit(0)
