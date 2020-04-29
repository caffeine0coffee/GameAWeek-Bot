import textwrap


class UserNotifyException(Exception):
    """ discordユーザーに通知する例外クラス """

    post_msg = ""


class WrongMessageFormatException(UserNotifyException):
    """ 宣言ポストの形式が間違っている場合の例外 """

    def __init__(self):
        self.post_msg = textwrap.dedent(
            """
        宣言の形式が間違っています
        形式は以下の通りです:
            
            //TODO (or //todo)
            タスク達成までの時間
            タスクの内容
        """
        )


class WrongTimeDurationException(UserNotifyException):
    """ 宣言ポストのタスク達成までの時間の記述形式が間違っている場合の例外 """

    def __init__(self):
        self.post_msg = textwrap.dedent(
            """
            時間の形式が間違っています
            時間の形式は以下の通りです:
            
                ??d ??h ??m ??s
            
            ただし:
                ・日, 時間, 分, 秒の間のスペースは任意
                ・d/h/m/s は D/H/M/S で代用可能
                ・必要に応じて日, 時間, 分, 秒を省略可能

            例:
                1h30m
                7d
                5m30s
                12H 32M 40S
            """
        )


class WrongArgumentFormatException(UserNotifyException):
    """ heygaw コマンドの引数のフォーマットが間違っている場合の例外 """

    def __init__(self):
        self.post_msg = textwrap.dedent(
            """
            引数の書式が正しくありません
            引数は
            
                arg, -a, --arg

            のいずれかの形式で記述してください
            また、値を必要とするオプションは複数同時に指定できません
        """
        )


class CommandNotFoundException(UserNotifyException):
    """ heygaw コマンドで該当するファンクションが見つからなかった場合の例外 """

    def __init__(self, func_name):
        self.post_msg = textwrap.dedent(
            """
            コマンド ' {} ' が見つかりません
            使用可能なコマンドの一覧は

                heygaw commands

            でご覧ください
        """.format(
                func_name
            )
        )


class ArgumentValueNotSpecifiedException(UserNotifyException):
    """ heygaw コマンドでオプションに対する値が指定されなかった場合の例外 """

    def __init__(self, bad_option_list):
        self.post_msg = textwrap.dedent(
            """
            引数 ' {} ' に対する値が指定されていません
            それぞれのコマンドに対するヘルプは

                heygaw [command] --help

            でご覧ください
        """
        )
