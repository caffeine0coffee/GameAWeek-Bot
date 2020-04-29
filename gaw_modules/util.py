import datetime
import re
import gaw_modules.exception as gaw_expt


class schedule:
    def __init__(self, start_time, duration, task, msg_src):
        self.start_time = start_time
        self.duration = duration
        self.end_time = start_time + duration
        self.task = task
        self.user = msg_src.author.display_name
        self.author = msg_src.author

    def show(self):
        print("start time is: " + str(self.start_time))
        print("duration is: " + str(self.duration))
        print("end time is: " + str(self.end_time))
        print("task is:")
        print(self.task)

    def __datetime_to_str(self, dt_src):
        res = dt_src.strftime("%Y年 %m月%d日(%a) %p%I時%M分%S秒")
        return res

    def get_accepted_message(self, msg_src):
        msg = ""
        msg += "宣言を受け付けました！\n"
        msg += "> ユーザー: " + self.user + "\n"
        msg += "> 期限: " + self.get_end_time() + "\n"
        msg += "頑張って！"
        return msg

    def get_start_time(self):
        return self.__datetime_to_str(self.start_time)

    def get_end_time(self):
        return self.__datetime_to_str(self.end_time)


def create_schedule(msg_src):
    src_lines = msg_src.content.split("\n")
    if len(src_lines) < 3:
        raise gaw_expt.WrongMessageFormatException
    duration = create_duration_datetime(src_lines[1])
    now = datetime.datetime.now()
    task = "\n".join(src_lines[2:])
    return schedule(now, duration, task, msg_src)


def create_duration_datetime(time_text):
    if not re.fullmatch(
        "(\s)*(\d\d?d)?(\s)*(\d\d?h)?(\s)*(\d\d?m)?(\s)*(\d\d?s)?", time_text
    ):
        raise gaw_expt.WrongTimeDurationException
    time_text = time_text.replace(" ", "").lower()

    breaks = ["d", "h", "m", "s"]
    elems = []
    for i in breaks:
        if i in time_text:
            spl = time_text.split(i)
            elems.append(int(spl[0]))
            time_text = spl[1]
        else:
            elems.append(0)
    return datetime.timedelta(
        days=elems[0], hours=elems[1], minutes=elems[2], seconds=elems[3]
    )


schedule_list = []
