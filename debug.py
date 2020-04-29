import main

with open("./debug_input.txt") as fin:
    content = fin.read()
    print("--- src_text is:")
    print(content, end='')

    try:
        result = main.create_schedule(content)
    except main.UserNotifyException as e:
        print(e.post_msg)
        exit(2)

    print("--- result is:")
    result.show()
