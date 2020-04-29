import textwrap

import gaw_modules.exception as gaw_expt
import gaw_modules.util as gaw_util


class GawFunction:
    # None: not executable
    # function's name as the command: executable
    func_name = None

    @classmethod
    async def exec_func(cls, discord_msg, args):
        pass


class GawFunctionHasDashArgs(GawFunction):
    func_name = None

    @classmethod
    def create_args_dic(cls, args, fopt_list):
        if not args:
            return []

        res = dict()
        try:
            i = 0
            while i < len(args):
                if args[i].startswith("-"):
                    if args[i].startswith("--"):
                        opt = args[i][2:]
                        if opt in fopt_list:
                            res[opt] = "flag"
                        else:
                            res[opt] = []
                    else:
                        opt = None
                        for w in args[i][1:]:
                            if w in fopt_list:
                                res[w] = "flag"
                            else:
                                if opt:
                                    raise gaw_expt.WrongArgumentFormatException
                                opt = w
                                res[opt] = []

                    if opt and res[opt] == []:
                        for j in range(i + 1, len(args)):
                            if args[j].startswith("-"):
                                break
                            res[opt].append(args[j])
                            i = i + 1

                else:
                    res[args[i]] = "value"

                i = i + 1

        except IndexError:
            raise gaw_expt.WrongArgumentFormatException
        return res


class ShowScheduleList(GawFunctionHasDashArgs):
    func_name = "list"

    @classmethod
    async def exec_func(cls, discord_msg, args):
        args_dic = super().create_args_dic(args, ["v", "help"])

        varbose_flg = "v" in args_dic
        # empty: show everyone
        user_show = [] if "u" not in args_dic else args_dic["u"]
        res = ""

        if "help" in args_dic:
            res = textwrap.dedent(
                """
                まだ終了時刻に達してない宣言の一覧を表示します
                オプション:
                    -v : 表示内容を多くします
                    -u [user1] [user2] ... : 表示するユーザーを限定します
                        ユーザー名はこのサーバーの表示名(ニックネームです)
                    --help : このヘルプを表示します
            """
            )
        else:
            for s in gaw_util.schedule_list:
                if not user_show or s.user in user_show:
                    res += s.user + "の宣言\n"
                    res += "> " + s.get_end_time() + " 締め切り\n"
                    if varbose_flg:
                        res += "> " + s.task + "\n"

        if not res:
            res = "(´・ω・`)"
        await discord_msg.channel.send(res)


class ShowCommands(GawFunction):
    func_name = "commands"

    @classmethod
    async def exec_func(cls, discord_msg, args):
        res = ""

        for f in function_list:
            res += f.func_name
            res += " "
        res += "\n"
        res += textwrap.dedent(
            """
            それぞれのコマンドのヘルプは

                heygaw <コマンド> --help

            をご覧ください
        """
        )

        await discord_msg.channel.send(res)


async def exec_gaw_func(discord_msg, command, args):
    print(function_list)
    for f in function_list:
        if f.func_name == command:
            await f.exec_func(discord_msg, args)
            return
    raise gaw_expt.CommandNotFoundException(command)


function_list = []


def init():
    search_all_function(GawFunction.__subclasses__())


def search_all_function(subcls_list):
    for f in subcls_list:
        search_all_function(f.__subclasses__())
        if f.func_name:
            function_list.append(f)
