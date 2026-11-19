
# HTML TAG, ATTRIBUTE, AND VALUE LEXICAL ANALYZER
# DFA Implementation using Python

class HTMLDFA:

    def __init__(self):
        self.tokens = []
        self.errors = []

    # Get the line and column position
    def get_position(self, text, index):
        line = text.count("\n", 0, index) + 1
        last_newline = text.rfind("\n", 0, index)
        column = index - last_newline
        return line, column

    # Add recognized token
    def add_token(self, token_type, lexeme, text, start):
        line, column = self.get_position(text, start)

        self.tokens.append({
            "type": token_type,
            "lexeme": lexeme,
            "line": line,
            "column": column
        })

    # Add lexical error
    def add_error(self, message, text, position):
        line, column = self.get_position(text, position)

        self.errors.append(
            f"{message} at line {line}, column {column}"
        )

    # DFA Scanner
    def scan(self, html):

        self.tokens = []
        self.errors = []

        i = 0
        length = len(html)

        state = "DATA"

        tag_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_:"
        attr_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_:."

        while i < length:

            char = html[i]

            # STATE 1: DATA
            # Reads text outside HTML tags
            if state == "DATA":

                if char == "<":
                    self.add_token(
                        "OPEN_BRACKET", "<", html, i
                    )
                    i += 1
                    state = "TAG_OPEN"

                else:
                    start = i

                    while i < length and html[i] != "<":
                        i += 1

                    self.add_token(
                        "TEXT", html[start:i], html, start
                    )

            # STATE 2: TAG_OPEN
            # Checks the beginning of a tag
            elif state == "TAG_OPEN":

                if char == "/":
                    self.add_token(
                        "SLASH", "/", html, i
                    )
                    i += 1
                    state = "TAG_NAME_START"

                elif char in tag_chars[:52]:
                    start = i
                    state = "TAG_NAME"

                else:
                    self.add_error(
                        "Invalid character after <",
                        html, i
                    )
                    i += 1
                    state = "DATA"

            # STATE 3: TAG_NAME_START
            # Reads the name after a closing-tag slash
            elif state == "TAG_NAME_START":

                if char in tag_chars[:52]:
                    state = "TAG_NAME"
                else:
                    self.add_error(
                        "Missing or invalid tag name",
                        html, i
                    )
                    state = "DATA"

            # STATE 4: TAG_NAME
            # Recognizes the HTML tag name
            elif state == "TAG_NAME":

                start = i

                while i < length and html[i] in tag_chars:
                    i += 1

                if i > start:
                    self.add_token(
                        "TAG_NAME", html[start:i], html, start
                    )

                state = "BEFORE_ATTR"

            # STATE 5: BEFORE_ATTR
            # Checks for attributes or closing bracket
            elif state == "BEFORE_ATTR":

                if char.isspace():
                    i += 1

                elif char == ">":
                    self.add_token(
                        "CLOSE_BRACKET", ">", html, i
                    )
                    i += 1
                    state = "DATA"

                elif char == "/":
                    self.add_token(
                        "SLASH", "/", html, i
                    )
                    i += 1
                    state = "SELF_CLOSING"

                elif char in attr_chars:
                    state = "ATTRIBUTE_NAME"

                else:
                    self.add_error(
                        "Invalid attribute character",
                        html, i
                    )
                    i += 1

            # STATE 6: ATTRIBUTE_NAME
            # Recognizes attribute names
            elif state == "ATTRIBUTE_NAME":

                start = i

                while i < length and html[i] in attr_chars:
                    i += 1

                self.add_token(
                    "ATTRIBUTE_NAME",
                    html[start:i],
                    html,
                    start
                )

                state = "AFTER_ATTR_NAME"

            # STATE 7: AFTER_ATTR_NAME
            # Checks for equals sign
            elif state == "AFTER_ATTR_NAME":

                if char.isspace():
                    i += 1

                elif char == "=":
                    self.add_token(
                        "EQUALS", "=", html, i
                    )
                    i += 1
                    state = "BEFORE_VALUE"

                elif char == ">":
                    self.add_token(
                        "CLOSE_BRACKET", ">", html, i
                    )
                    i += 1
                    state = "DATA"

                elif char == "/":
                    self.add_token(
                        "SLASH", "/", html, i
                    )
                    i += 1
                    state = "SELF_CLOSING"

                elif char in attr_chars:
                    # Boolean attribute
                    state = "ATTRIBUTE_NAME"

                else:
                    self.add_error(
                        "Invalid character after attribute name",
                        html, i
                    )
                    i += 1

            # STATE 8: BEFORE_VALUE
            # Checks the attribute value format
            elif state == "BEFORE_VALUE":

                if char.isspace():
                    i += 1

                elif char == '"':
                    start = i
                    i += 1
                    state = "DOUBLE_QUOTED_VALUE"

                elif char == "'":
                    start = i
                    i += 1
                    state = "SINGLE_QUOTED_VALUE"

                elif char == ">":
                    self.add_error(
                        "Missing attribute value",
                        html, i
                    )
                    i += 1
                    state = "DATA"

                else:
                    start = i
                    state = "UNQUOTED_VALUE"

            # STATE 9: DOUBLE_QUOTED_VALUE
            elif state == "DOUBLE_QUOTED_VALUE":

                if char == '"':
                    i += 1

                    self.add_token(
                        "ATTRIBUTE_VALUE",
                        html[start:i],
                        html,
                        start
                    )

                    state = "BEFORE_ATTR"

                else:
                    i += 1

            # STATE 10: SINGLE_QUOTED_VALUE
            elif state == "SINGLE_QUOTED_VALUE":

                if char == "'":
                    i += 1

                    self.add_token(
                        "ATTRIBUTE_VALUE",
                        html[start:i],
                        html,
                        start
                    )

                    state = "BEFORE_ATTR"

                else:
                    i += 1

            # STATE 11: UNQUOTED_VALUE
            elif state == "UNQUOTED_VALUE":

                if char.isspace():
                    self.add_token(
                        "ATTRIBUTE_VALUE",
                        html[start:i],
                        html,
                        start
                    )

                    state = "BEFORE_ATTR"

                elif char == ">":
                    self.add_token(
                        "ATTRIBUTE_VALUE",
                        html[start:i],
                        html,
                        start
                    )

                    self.add_token(
                        "CLOSE_BRACKET", ">", html, i
                    )

                    i += 1
                    state = "DATA"

                else:
                    i += 1

            # STATE 12: SELF_CLOSING
            elif state == "SELF_CLOSING":

                if char == ">":
                    self.add_token(
                        "CLOSE_BRACKET", ">", html, i
                    )
                    i += 1
                    state = "DATA"

                else:
                    self.add_error(
                        "Expected > after /",
                        html, i
                    )
                    i += 1
                    state = "DATA"

        # Check unfinished states at the end of input
        if state == "DOUBLE_QUOTED_VALUE":
            self.add_error(
                "Unclosed double quotation mark",
                html, start
            )

        elif state == "SINGLE_QUOTED_VALUE":
            self.add_error(
                "Unclosed single quotation mark",
                html, start
            )

        elif state == "TAG_OPEN" or state == "TAG_NAME_START":
            self.add_error(
                "Incomplete HTML tag",
                html, length
            )

        elif state in ("TAG_NAME", "BEFORE_ATTR",
                       "ATTRIBUTE_NAME", "AFTER_ATTR_NAME",
                       "BEFORE_VALUE", "SELF_CLOSING"):
            self.add_error(
                "Unclosed or incomplete HTML tag",
                html, length
            )

        elif state == "UNQUOTED_VALUE":
            self.add_token(
                "ATTRIBUTE_VALUE",
                html[start:length],
                html,
                start
            )
            self.add_error(
                "HTML tag is missing closing >",
                html, length
            )

        return self.tokens, self.errors


# ==========================================
# MAIN PROGRAM
# ==========================================

def main():

    lexer = HTMLDFA()

    # Five sample strings
    samples = [
        '<h1>Hello world</h1>',
        '<div class="container">',
        '<img src="plant.png">',
        '<img src="plant.png" alt="Plant">',
        '<div class="container"><p>Hello</p></div>'
    ]

    print("=" * 65)
    print(" HTML TAG, ATTRIBUTE, AND VALUE LEXICAL ANALYZER")
    print(" DFA IMPLEMENTATION")
    print("=" * 65)

    while True:

        print("\nSELECT AN OPTION:")
        print("1. Test Sample Strings")
        print("2. Enter Your Own HTML String")
        print("3. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":

            for number, sample in enumerate(samples, 1):

                tokens, errors = lexer.scan(sample)

                print("\n" + "=" * 65)
                print(f"SAMPLE STRING {number}")
                print("=" * 65)

                print("INPUT:", sample)

                if errors:
                    print("\nSTATUS: REJECTED")
                else:
                    print("\nSTATUS: ACCEPTED")

                print("\nTOKEN OUTPUT:")
                print("-" * 65)
                print(f"{'TOKEN TYPE':<22} {'LEXEME':<22} POSITION")
                print("-" * 65)

                for token in tokens:
                    print(
                        f"{token['type']:<22} "
                        f"{token['lexeme']:<22} "
                        f"{token['line']}:{token['column']}"
                    )

                if errors:
                    print("\nLEXICAL ERRORS:")
                    for error in errors:
                        print(" -", error)

        elif choice == "2":

            html = input("\nEnter HTML string: ")

            tokens, errors = lexer.scan(html)

            print("\n" + "=" * 65)
            print("LEXICAL ANALYSIS RESULT")
            print("=" * 65)

            if errors:
                print("STATUS: REJECTED")
            else:
                print("STATUS: ACCEPTED")

            print("\nTOKEN OUTPUT:")
            print("-" * 65)
            print(f"{'TOKEN TYPE':<22} {'LEXEME':<22} POSITION")
            print("-" * 65)

            for token in tokens:
                print(
                    f"{token['type']:<22} "
                    f"{token['lexeme']:<22} "
                    f"{token['line']}:{token['column']}"
                )

            if errors:
                print("\nLEXICAL ERRORS:")
                for error in errors:
                    print(" -", error)

        elif choice == "3":
            print("\nThank you for using the Lexical Analyzer!")
            break

        else:
            print("\nInvalid choice. Please try again.")


if __name__ == "__main__":
    main()
