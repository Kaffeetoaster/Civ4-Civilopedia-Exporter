
unicode = type(u"")


def write_json(obj, filename):
    f = open(filename, "w")
    f.write(to_json(obj))
    f.close()


def escape_json_string(value):
    if isinstance(value, str):
        try:
            value = value.decode("utf-8")
        except UnicodeDecodeError:
            value = value.decode("latin-1")
    elif not isinstance(value, unicode):
        value = unicode(value)

    pieces = []
    for character in value:
        codepoint = ord(character)
        if character == '"':
            pieces.append('\\"')
        elif character == '\\':
            pieces.append('\\\\')
        elif character == '\b':
            pieces.append('\\\\b')
        elif character == '\f':
            pieces.append('\\\\f')
        elif character == '\n':
            pieces.append('\\\\n')
        elif character == '\r':
            pieces.append('\\\\r')
        elif character == '\t':
            pieces.append('\\\\t')
        elif codepoint < 0x20 or codepoint > 0x7E:
            if codepoint <= 0xFFFF:
                pieces.append('\\\\u%04x' % codepoint)
            else:
                codepoint -= 0x10000
                high_surrogate = 0xD800 + (codepoint >> 10)
                low_surrogate = 0xDC00 + (codepoint & 0x3FF)
                pieces.append('\\\\u%04x\\\\u%04x' % (high_surrogate, low_surrogate))
        else:
            pieces.append(character)

    return '"' + ''.join(pieces) + '"'


def to_json(obj):
    # dict
    if isinstance(obj, dict):
        items = []
        for k, v in obj.items():
            items.append('"%s":%s' % (k, to_json(v)))
        return '{' + ','.join(items) + '}'

    # list / tuple
    elif isinstance(obj, (list, tuple)):
        return '[' + ','.join([to_json(x) for x in obj]) + ']'

    # string
    elif isinstance(obj, (str, unicode)):
        return escape_json_string(obj)

    # boolean
    elif obj is True:
        return "true"
    elif obj is False:
        return "false"

    # None
    elif obj is None:
        return "null"

    # numbers
    else:
        return str(obj)
    
    