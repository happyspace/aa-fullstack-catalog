from sample.markdown_adapter import run_markdown


def test_non_marked_lines():
    print('in test_non_marked_lines')
    assert run_markdown('this line has no special handling') == \
        '<p>this line has no special handling</p>'


if __name__ == '__main__':
    test_non_marked_lines()
