# Tests

Tests are put in this folder.

Feel free to add more, the more the better!

## How to run the tests

```bash
pipenv install --dev
make test
```

And you should see

```
................................
Name                    Stmts   Miss Branch BrPart  Cover
---------------------------------------------------------
mackup/__init__.py          0      0      0      0   100%
mackup/application.py      88     79     62      0     7%
mackup/appsdb.py           78     17     38     12    66%
mackup/config.py           92      3     34      2    96%
mackup/constants.py        15      0      0      0   100%
mackup/mackup.py           37     22     14      0    33%
mackup/main.py             77     61     32      0    17%
mackup/utils.py           148      7     58     13    90%
---------------------------------------------------------
TOTAL                     535    189    238     27    58%
----------------------------------------------------------------------
Ran 32 tests in 0.178s

OK
```

Yeah, I wrote this file when there was only 1 test, I hope there will be more
when you read it!
