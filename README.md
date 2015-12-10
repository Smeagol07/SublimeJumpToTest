Sublime Text - Jump To Test
===========================


Overview
--------
Plugin provides quick switch option between test and tested class.<br />
I'ts preconfigured to work with ruby test and spec, but can work with almost anything.

Installation
------------
With [Package Control](http://wbond.net/sublime_packages/package_control):

It's on my todo list :)

Manually:

1. Go into your packages folder (in ST, find Browse Packages... menu item to open this folder)
2. Clone repository `git clone https://github.com/Smeagol07/SublimeJumpToTest.git JumpToTest`
3. Restart ST editor (if required, probably not)

How it works?
-------------
Script is looking for test file related to current class (or the other way). To be fair it can jump to any related file, ie. form .css to .scss or from .coffe to .js. All you have to do is setup correct patterns. By defult its configured for Ruby test `ctrl+shift+.` and spec `ctrl+shift+,` files.

Configuration
-------------

1. Patterns:

Patterns can be set up in configuration files, and are looking like that:
```
  "jtt_pattens": [{
    "name": "ruby_test",
    "re_check_full_path": false,
    "re_check_type": ".+.rb$",
    "re_is_test": ".+_test.rb$",
    "re_from_test": ["(.+)_test\\.rb$", "\\1.rb"],
    "re_to_test": ["(.+)\\.rb$", "\\1_test.rb"]
  }, {
    "name": "ruby_spec",
    "re_check_full_path": false,
    "re_check_type": ".+.rb$",
    "re_is_test": ".+_spec.rb$",
    "re_from_test": ["(.+)_spec\\.rb$", "\\1.rb"],
    "re_to_test": ["(.+)\\.rb$", "\\1_spec.rb"]
  }]
```
Patterns are checked in order from configuration and if one match the rest is not checked.
- `name` - can be used in keymap configuration (by defoult `ctrl+shift+.` jumps to test file and `ctrl+shift+,` to spec).
- `re_check_full_path` - if `true` file will be check by the full path otherwise only name will be passed to regexps.
- `re_check_type` - regexp to check if pattern match file type.
- `re_is_test` - regexp to find out if current file is a test or a tested class.
- `re_from_test` - regex to transform test file name to tested class file name
- `re_to_test` - regex to transform from tested class file name to test file name

2. Keymap

Different keys can be configured to use different patterns.
```
[{
    "keys": ["super+shift+."],
    "command": "jump_to_test",
    "context": [{
        "key": "selector",
        "operator": "equal",
        "operand": "source.ruby"
    }],
}, {
    "keys": ["super+shift+,"],
    "command": "jump_to_test",
    "args": {
        "pattern_name": "ruby_spec"
    },
    "context": [{
        "key": "selector",
        "operator": "equal",
        "operand": "source.ruby"
    }],
}]
```
- `pattern_name` should match the `name` attribute defined in `jtt_patterns`


Note
----
I've been inspired by https://github.com/ahare/GoToTest<br />
And I've copied bits and pieces from https://github.com/gs/sublime-text-go-to-file

License
-------
WTFPL (http://www.wtfpl.net/) - I dont give a damn.
