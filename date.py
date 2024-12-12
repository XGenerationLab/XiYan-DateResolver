import re
import calendar
from datetime import datetime, timedelta, date
from typing import List
from dateutil.relativedelta import relativedelta


class DateTimeUtil:
    SPECIFIC_YEAR_MONTH_DAY_PATTERN = re.compile(r'\d{4}年\d{2}月\d{2}日')
    GENERAL_YEAR_MONTH_DAY_PATTERN = re.compile(r'(今年|去年|前年|明年|后年)(\d{2}月\d{2}日)')
    GENERAL_MONTH_DAY_PATTERN = re.compile(r'(本月|上月|上上月|下月)(\d{2}日)')
    GENERAL_DAY_PATTERN = re.compile(r'(今天|昨天|前天|明天|后天|上月今天|上上月今天)')
    # 每周从周一开始算
    WEEK_DAY_PATTERN = re.compile(r'本周第(\d)天')
    GENERAL_MONTH_LAST_DAY_PATTERN = re.compile(r'(本月|上月)最后一天')
    GENERAL_YEAR_MONTH_LAST_DAY_PATTERN = re.compile(r'(今年)(\d{2})月最后一天')
    SPECIFIC_YEAR_MONTH_PATTERN = re.compile(r'\d{4}年\d{2}月')
    GENERAL_YEAR_MONTH_PATTERN = re.compile(r'(今年|去年|前年|明年|后年)(\d{2}月)')
    GENERAL_MONTH_PATTERN = re.compile(r'(本月|上月|上上月|下月|去年本月)')
    SPECIFIC_YEAR_PATTERN = re.compile(r'(\d{4})年')
    GENERAL_YEAR_PATTERN = re.compile(r'(今年|去年|前年|明年|后年)')
    SPECIFIC_YEAR_QUARTER_PATTERN = re.compile(r'\d{4}年第\d季度')
    # 今年第1季度 = 2024年第1季度
    GENERAL_YEAR_QUARTER_PATTERN = re.compile(r'(今年|去年|前年|明年|后年)(第\d季度)')
    GENERAL_QUARTER_PATTERN = re.compile(r'(本季度|上季度|下季度|去年本季度)')
    GENERAL_WEEK_SPECIFIC_DAY_PATTERN = re.compile(r'(本周|上周|上上周|下周|下下周)星期(\d)')
    GENERAL_WEEK_PATTERN = re.compile(r'(本周|上周|上上周|下周|下下周)')
    SPECIFIC_YEAR_WEEK_PATTERN = re.compile(r'(\d{4})年第(\d{2})周')
    # 今年第54周会输出一个错的，第53周是对的，会截取到今天
    GENERAL_YEAR_WEEK_PATTERN = re.compile(r'(今年|去年|前年)第(\d{2})周')
    # 和上面同理
    GENERAL_MONTH_WEEK_PATTERN = re.compile(r'(本月|上月)第(\d)周')
    SPECIFIC_YEAR_MONTH_LAST_WEEK_PATTERN = re.compile(r'(\d{4})年(\d{2})月最后一周')
    GENERAL_MONTH_LAST_WEEK_PATTERN = re.compile(r'(本月|上月|上上月)最后一周')
    SPECIFIC_YEAR_MONTH_WEEK_PATTERN = re.compile(r'(\d{4})年(\d{2})月第(\d)周')
    GENERAL_YEAR_MONTH_WEEK_PATTERN = re.compile(r'(今年|去年|前年)(\d{2})月第(\d)周')
    SPECIFIC_YEAR_MONTH_COMPLETE_WEEK_PATTERN = re.compile(r'(\d{4})年(\d{2})月第(\d)个完整周')
    GENERAL_YEAR_COMPLETE_WEEK_PATTERN = re.compile(r'(今年|去年|前年)第(\d{2})个完整周')
    SPECIFIC_YEAR_COMPLETE_WEEK_PATTERN = re.compile(r'(\d{4})年第(\d{2})个完整周')
    GENERAL_YEAR_MONTH_COMPLETE_WEEK_PATTERN = re.compile(r'(今年|去年|前年)(\d{2})月第(\d)个完整周')
    GENERAL_MONTH_COMPLETE_WEEK_PATTERN = re.compile(r'(本月|上月)第(\d)个完整周')
    # GENERAL_MONTH_LAST_COMPLETE_WEEK_PATTERN = re.compile(r'(本月|上月|上上月)最后一个完整周')
    RECENT_N_YEAR_PATTERN = re.compile(r'近(\d+)年')
    RECENT_N_MONTH_PATTERN = re.compile(r'近(\d+)个月')
    RECENT_N_WEEK_PATTERN = re.compile(r'近(\d+)周')
    RECENT_N_DAY_PATTERN = re.compile(r'近(\d+)天')
    RECENT_N_COMPLETE_YEAR_PATTERN = re.compile(r'近(\d+)个完整年')
    RECENT_N_COMPLETE_QUARTER_PATTERN = re.compile(r'近(\d+)个完整季度')
    RECENT_N_COMPLETE_MONTH_PATTERN = re.compile(r'近(\d+)个完整月')
    RECENT_N_COMPLETE_WEEK_PATTERN = re.compile(r'近(\d+)个完整周')
    RECENT_N_DAY_WITHOUT_TODAY_PATTERN = re.compile(r'不包含今天的近(\d+)天')
    RECENT_N_QUARTER_WITH_CURRENT_PATTERN = re.compile(r'包含当前季度的近(\d+)个季度')
    SPECIFIC_YEAR_HALF_YEAR_PATTERN = re.compile(r'(\d{4})年(上|下)半年')
    GENERAL_YEAR_HALF_YEAR_PATTERN = re.compile(r'(今年|去年)(上|下)半年')
    HALF_YEAR_PATTERN = re.compile(r'(上|下)半年')

    @staticmethod
    def build_date_time_comment(expressions: List[str]) -> str:
        now = datetime.now()
        year = now.year
        month = now.month
        day = now.day
        quarter = (month - 1) // 3 + 1
        today_comment = f"今天是{year}年{month:02d}月{day:02d}日，是{year}年的第{quarter}季度"

        date_time_comment_list = DateTimeUtil.build_date_expressions(expressions, now)
        final_expression = [today_comment, "需要计算的时间是："] + date_time_comment_list
        return "\n".join(final_expression)

    @staticmethod
    def build_date_expressions(expressions: List[str], now: date) -> List[str]:
        date_time_comment_list = []

        for expression in expressions:
            if DateTimeUtil.SPECIFIC_YEAR_HALF_YEAR_PATTERN.match(expression):
                year_ex = int(DateTimeUtil.SPECIFIC_YEAR_HALF_YEAR_PATTERN.match(expression).group(1))
                half_year_ex = DateTimeUtil.SPECIFIC_YEAR_HALF_YEAR_PATTERN.match(expression).group(2)
                comment = DateTimeUtil.get_specific_year_half_year_ex(now, year_ex, half_year_ex)
                date_time_comment_list.append(f"{expression}={comment}")
                continue

            if DateTimeUtil.GENERAL_YEAR_HALF_YEAR_PATTERN.match(expression):
                year_ex = DateTimeUtil.GENERAL_YEAR_HALF_YEAR_PATTERN.match(expression).group(1)
                half_year_ex = DateTimeUtil.GENERAL_YEAR_HALF_YEAR_PATTERN.match(expression).group(2)
                comment = DateTimeUtil.get_general_year_half_year_ex(now, year_ex, half_year_ex)
                date_time_comment_list.append(f"{expression}={comment}")
                continue

            if DateTimeUtil.HALF_YEAR_PATTERN.match(expression):
                half_year_ex = DateTimeUtil.HALF_YEAR_PATTERN.match(expression).group(1)
                comment = DateTimeUtil.get_specific_year_half_year_ex(now, now.year, half_year_ex)
                date_time_comment_list.append(f"{expression}={comment}")
                continue

            if DateTimeUtil.SPECIFIC_YEAR_MONTH_COMPLETE_WEEK_PATTERN.match(expression):
                year_ex = int(DateTimeUtil.SPECIFIC_YEAR_MONTH_COMPLETE_WEEK_PATTERN.match(expression).group(1))
                month_ex = int(DateTimeUtil.SPECIFIC_YEAR_MONTH_COMPLETE_WEEK_PATTERN.match(expression).group(2))
                week_ex = int(DateTimeUtil.SPECIFIC_YEAR_MONTH_COMPLETE_WEEK_PATTERN.match(expression).group(3))
                comment = DateTimeUtil.get_specific_year_month_complete_week_ex(now, year_ex, month_ex, week_ex)
                date_time_comment_list.append(f"{expression}={comment}")
                continue

            if DateTimeUtil.GENERAL_YEAR_MONTH_COMPLETE_WEEK_PATTERN.match(expression):
                year_ex = DateTimeUtil.GENERAL_YEAR_MONTH_COMPLETE_WEEK_PATTERN.match(expression).group(1)
                month_ex = int(DateTimeUtil.GENERAL_YEAR_MONTH_COMPLETE_WEEK_PATTERN.match(expression).group(2))
                week_ex = int(DateTimeUtil.GENERAL_YEAR_MONTH_COMPLETE_WEEK_PATTERN.match(expression).group(3))
                comment = DateTimeUtil.get_general_year_month_complete_week_ex(now, year_ex, month_ex, week_ex)
                date_time_comment_list.append(f"{expression}={comment}")
                continue

            if DateTimeUtil.SPECIFIC_YEAR_COMPLETE_WEEK_PATTERN.match(expression):
                year_ex = int(DateTimeUtil.SPECIFIC_YEAR_COMPLETE_WEEK_PATTERN.match(expression).group(1))
                week_ex = int(DateTimeUtil.SPECIFIC_YEAR_COMPLETE_WEEK_PATTERN.match(expression).group(2))
                comment = DateTimeUtil.get_specific_year_complete_week_ex(now, year_ex, week_ex)
                date_time_comment_list.append(f"{expression}={comment}")
                continue

            if DateTimeUtil.GENERAL_YEAR_COMPLETE_WEEK_PATTERN.match(expression):
                year_ex = DateTimeUtil.GENERAL_YEAR_COMPLETE_WEEK_PATTERN.match(expression).group(1)
                week_ex = int(DateTimeUtil.GENERAL_YEAR_COMPLETE_WEEK_PATTERN.match(expression).group(2))
                comment = DateTimeUtil.get_general_year_complete_week_ex(now, year_ex, week_ex)
                date_time_comment_list.append(f"{expression}={comment}")
                continue

            if DateTimeUtil.GENERAL_MONTH_COMPLETE_WEEK_PATTERN.match(expression):
                month_ex = DateTimeUtil.GENERAL_MONTH_COMPLETE_WEEK_PATTERN.match(expression).group(1)
                week_ex = int(DateTimeUtil.GENERAL_MONTH_COMPLETE_WEEK_PATTERN.match(expression).group(2))
                comment = DateTimeUtil.get_general_month_complete_week_ex(now, month_ex, week_ex)
                date_time_comment_list.append(f"{expression}={comment}")
                continue

            if DateTimeUtil.GENERAL_MONTH_WEEK_PATTERN.match(expression):
                month_ex = DateTimeUtil.GENERAL_MONTH_WEEK_PATTERN.match(expression).group(1)
                week_ex = int(DateTimeUtil.GENERAL_MONTH_WEEK_PATTERN.match(expression).group(2))
                comment = DateTimeUtil.get_general_month_week_ex(now, month_ex, week_ex)
                date_time_comment_list.append(f"{expression}={comment}")
                continue

            if DateTimeUtil.SPECIFIC_YEAR_MONTH_DAY_PATTERN.match(expression):
                date_time_comment_list.append(f"{expression}={expression}")
                continue

            if DateTimeUtil.GENERAL_YEAR_MONTH_DAY_PATTERN.match(expression):
                year_ex = DateTimeUtil.GENERAL_YEAR_MONTH_DAY_PATTERN.match(expression).group(1)
                comment = DateTimeUtil.get_year_ex(now, year_ex) + DateTimeUtil.GENERAL_YEAR_MONTH_DAY_PATTERN.match(
                    expression).group(2)
                date_time_comment_list.append(f"{expression}={comment}")
                continue

            if DateTimeUtil.GENERAL_MONTH_DAY_PATTERN.match(expression):
                month_ex = DateTimeUtil.GENERAL_MONTH_DAY_PATTERN.match(expression).group(1)
                comment = DateTimeUtil.get_month_ex(now, month_ex) + DateTimeUtil.GENERAL_MONTH_DAY_PATTERN.match(
                    expression).group(2)
                date_time_comment_list.append(f"{expression}={comment}")
                continue

            if DateTimeUtil.GENERAL_YEAR_MONTH_LAST_DAY_PATTERN.match(expression):
                year_ex = DateTimeUtil.GENERAL_YEAR_MONTH_LAST_DAY_PATTERN.match(expression).group(1)
                month_ex = DateTimeUtil.GENERAL_YEAR_MONTH_LAST_DAY_PATTERN.match(expression).group(2)
                comment = DateTimeUtil.get_general_year_month_last_day_ex(now, year_ex, int(month_ex))
                date_time_comment_list.append(f"{expression}={comment}")
                continue

            if DateTimeUtil.GENERAL_MONTH_LAST_DAY_PATTERN.match(expression):
                month_ex = DateTimeUtil.GENERAL_MONTH_LAST_DAY_PATTERN.match(expression).group(1)
                comment = DateTimeUtil.get_month_last_day_ex(now, month_ex)
                date_time_comment_list.append(f"{expression}={comment}")
                continue

            if DateTimeUtil.WEEK_DAY_PATTERN.match(expression):
                week_day = int(DateTimeUtil.WEEK_DAY_PATTERN.match(expression).group(1))
                comment = DateTimeUtil.get_week_day_ex(now, week_day)
                date_time_comment_list.append(f"{expression}={comment}")
                continue

            if DateTimeUtil.GENERAL_WEEK_SPECIFIC_DAY_PATTERN.match(expression):
                week_ex = DateTimeUtil.GENERAL_WEEK_SPECIFIC_DAY_PATTERN.match(expression).group(1)
                day = int(DateTimeUtil.GENERAL_WEEK_SPECIFIC_DAY_PATTERN.match(expression).group(2))
                comment = DateTimeUtil.get_general_week_day_ex(now, week_ex, day)
                date_time_comment_list.append(f"{expression}={comment}")
                continue

            if DateTimeUtil.SPECIFIC_YEAR_QUARTER_PATTERN.match(expression):
                date_time_comment_list.append(f"{expression}={expression}")
                continue

            if DateTimeUtil.GENERAL_YEAR_QUARTER_PATTERN.match(expression):
                year_ex = DateTimeUtil.GENERAL_YEAR_QUARTER_PATTERN.match(expression).group(1)
                quarter_ex = DateTimeUtil.GENERAL_YEAR_QUARTER_PATTERN.match(expression).group(2)
                comment = DateTimeUtil.get_year_ex(now, year_ex) + quarter_ex
                date_time_comment_list.append(f"{expression}={comment}")
                continue

            if DateTimeUtil.GENERAL_QUARTER_PATTERN.match(expression):
                quarter_ex = DateTimeUtil.GENERAL_QUARTER_PATTERN.match(expression).group(1)
                comment = DateTimeUtil.get_quarter_ex(now, quarter_ex)
                date_time_comment_list.append(f"{expression}={comment}")
                continue

            if DateTimeUtil.GENERAL_WEEK_PATTERN.match(expression):
                week_ex = DateTimeUtil.GENERAL_WEEK_PATTERN.match(expression).group(1)
                comment = DateTimeUtil.get_week_ex(now, week_ex)
                date_time_comment_list.append(f"{expression}={comment}")
                continue

            if DateTimeUtil.SPECIFIC_YEAR_WEEK_PATTERN.match(expression):
                year_ex = int(DateTimeUtil.SPECIFIC_YEAR_WEEK_PATTERN.match(expression).group(1))
                week_ex = int(DateTimeUtil.SPECIFIC_YEAR_WEEK_PATTERN.match(expression).group(2))
                comment = DateTimeUtil.get_specific_year_week_ex(now, year_ex, week_ex)
                date_time_comment_list.append(f"{expression}={comment}")
                continue

            if DateTimeUtil.GENERAL_YEAR_WEEK_PATTERN.match(expression):
                year_ex = DateTimeUtil.GENERAL_YEAR_WEEK_PATTERN.match(expression).group(1)
                week_ex = int(DateTimeUtil.GENERAL_YEAR_WEEK_PATTERN.match(expression).group(2))
                comment = DateTimeUtil.get_general_year_week_ex(now, year_ex, week_ex)
                date_time_comment_list.append(f"{expression}={comment}")
                continue

            if DateTimeUtil.SPECIFIC_YEAR_MONTH_WEEK_PATTERN.match(expression):
                year_ex = int(DateTimeUtil.SPECIFIC_YEAR_MONTH_WEEK_PATTERN.match(expression).group(1))
                month_ex = int(DateTimeUtil.SPECIFIC_YEAR_MONTH_WEEK_PATTERN.match(expression).group(2))
                week_ex = int(DateTimeUtil.SPECIFIC_YEAR_MONTH_WEEK_PATTERN.match(expression).group(3))
                comment = DateTimeUtil.get_specific_year_month_week_ex(now, year_ex, month_ex, week_ex)
                date_time_comment_list.append(f"{expression}={comment}")
                continue

            if DateTimeUtil.GENERAL_YEAR_MONTH_WEEK_PATTERN.match(expression):
                year_ex = DateTimeUtil.GENERAL_YEAR_MONTH_WEEK_PATTERN.match(expression).group(1)
                month_ex = int(DateTimeUtil.GENERAL_YEAR_MONTH_WEEK_PATTERN.match(expression).group(2))
                week_ex = int(DateTimeUtil.GENERAL_YEAR_MONTH_WEEK_PATTERN.match(expression).group(3))
                comment = DateTimeUtil.get_general_year_month_week_ex(now, year_ex, month_ex, week_ex)
                date_time_comment_list.append(f"{expression}={comment}")
                continue

            if DateTimeUtil.SPECIFIC_YEAR_MONTH_LAST_WEEK_PATTERN.match(expression):
                year_ex = int(DateTimeUtil.SPECIFIC_YEAR_MONTH_LAST_WEEK_PATTERN.match(expression).group(1))
                month_ex = int(DateTimeUtil.SPECIFIC_YEAR_MONTH_LAST_WEEK_PATTERN.match(expression).group(2))
                comment = DateTimeUtil.get_specific_year_month_last_week(now, year_ex, month_ex)
                date_time_comment_list.append(f"{expression}={comment}")
                continue

            if DateTimeUtil.GENERAL_MONTH_LAST_WEEK_PATTERN.match(expression):
                month_ex = DateTimeUtil.GENERAL_MONTH_LAST_WEEK_PATTERN.match(expression).group(1)
                comment = DateTimeUtil.get_general_month_last_week(now, month_ex)
                date_time_comment_list.append(f"{expression}={comment}")
                continue

            # if DateTimeUtil.GENERAL_MONTH_LAST_COMPLETE_WEEK_PATTERN.match(expression):
            #     month_ex = DateTimeUtil.GENERAL_MONTH_LAST_COMPLETE_WEEK_PATTERN.match(expression).group(1)
            #     comment = DateTimeUtil.get_general_month_last_complete_week_ex(now, month_ex)
            #     date_time_comment_list.append(f"{expression}={comment}")
            #     continue

            if DateTimeUtil.RECENT_N_YEAR_PATTERN.match(expression):
                n = int(DateTimeUtil.RECENT_N_YEAR_PATTERN.match(expression).group(1))
                comment = DateTimeUtil.get_recent_n_year(now, n)
                date_time_comment_list.append(f"{expression}={comment}")
                continue

            if DateTimeUtil.RECENT_N_MONTH_PATTERN.match(expression):
                n = int(DateTimeUtil.RECENT_N_MONTH_PATTERN.match(expression).group(1))
                comment = DateTimeUtil.get_recent_n_month(now, n)
                date_time_comment_list.append(f"{expression}={comment}")
                continue

            if DateTimeUtil.RECENT_N_WEEK_PATTERN.match(expression):
                n = int(DateTimeUtil.RECENT_N_WEEK_PATTERN.match(expression).group(1))
                comment = DateTimeUtil.get_recent_n_week(now, n)
                date_time_comment_list.append(f"{expression}={comment}")
                continue

            if DateTimeUtil.RECENT_N_DAY_WITHOUT_TODAY_PATTERN.match(expression):
                n = int(DateTimeUtil.RECENT_N_DAY_WITHOUT_TODAY_PATTERN.match(expression).group(1))
                comment = DateTimeUtil.get_recent_n_day_without_today(now, n)
                date_time_comment_list.append(f"{expression}={comment}")
                continue

            if DateTimeUtil.RECENT_N_DAY_PATTERN.match(expression):
                n = int(DateTimeUtil.RECENT_N_DAY_PATTERN.match(expression).group(1))
                comment = DateTimeUtil.get_recent_n_day(now, n)
                date_time_comment_list.append(f"{expression}={comment}")
                continue

            if DateTimeUtil.RECENT_N_COMPLETE_YEAR_PATTERN.match(expression):
                n = int(DateTimeUtil.RECENT_N_COMPLETE_YEAR_PATTERN.match(expression).group(1))
                comment = DateTimeUtil.get_recent_n_complete_year(now, n)
                date_time_comment_list.append(f"{expression}={comment}")
                continue

            if DateTimeUtil.RECENT_N_COMPLETE_QUARTER_PATTERN.match(expression):
                n = int(DateTimeUtil.RECENT_N_COMPLETE_QUARTER_PATTERN.match(expression).group(1))
                comment = DateTimeUtil.get_recent_n_complete_quarter(now, n)
                date_time_comment_list.append(f"{expression}={comment}")
                continue

            if DateTimeUtil.RECENT_N_COMPLETE_MONTH_PATTERN.match(expression):
                n = int(DateTimeUtil.RECENT_N_COMPLETE_MONTH_PATTERN.match(expression).group(1))
                comment = DateTimeUtil.get_recent_n_complete_month(now, n)
                date_time_comment_list.append(f"{expression}={comment}")
                continue

            if DateTimeUtil.RECENT_N_COMPLETE_WEEK_PATTERN.match(expression):
                n = int(DateTimeUtil.RECENT_N_COMPLETE_WEEK_PATTERN.match(expression).group(1))
                comment = DateTimeUtil.get_recent_n_complete_week(now, n)
                date_time_comment_list.append(f"{expression}={comment}")
                continue

            if DateTimeUtil.RECENT_N_QUARTER_WITH_CURRENT_PATTERN.match(expression):
                n = int(DateTimeUtil.RECENT_N_QUARTER_WITH_CURRENT_PATTERN.match(expression).group(1))
                comment = DateTimeUtil.get_recent_n_quarter_with_current(now, n)
                date_time_comment_list.append(f"{expression}={comment}")
                continue

            if DateTimeUtil.SPECIFIC_YEAR_MONTH_PATTERN.match(expression):
                date_time_comment_list.append(f"{expression}={expression}")
                continue

            if DateTimeUtil.GENERAL_YEAR_MONTH_PATTERN.match(expression):
                year_ex = DateTimeUtil.GENERAL_YEAR_MONTH_PATTERN.match(expression).group(1)
                comment = DateTimeUtil.get_year_ex(now, year_ex) + DateTimeUtil.GENERAL_YEAR_MONTH_PATTERN.match(expression).group(2)
                date_time_comment_list.append(f"{expression}={comment}")
                continue

            if DateTimeUtil.GENERAL_DAY_PATTERN.match(expression):
                day_ex = DateTimeUtil.GENERAL_DAY_PATTERN.match(expression).group(1)
                comment = DateTimeUtil.get_day_ex(now, day_ex)
                date_time_comment_list.append(f"{expression}={comment}")
                continue

            if DateTimeUtil.GENERAL_MONTH_PATTERN.match(expression):
                month_ex = DateTimeUtil.GENERAL_MONTH_PATTERN.match(expression).group(1)
                comment = DateTimeUtil.get_month_ex(now, month_ex)
                date_time_comment_list.append(f"{expression}={comment}")
                continue

            if DateTimeUtil.SPECIFIC_YEAR_PATTERN.match(expression):
                year_ex = int(DateTimeUtil.SPECIFIC_YEAR_PATTERN.match(expression).group(1))
                comment = f"{year_ex}年"
                date_time_comment_list.append(f"{expression}={comment}")
                continue

            if DateTimeUtil.GENERAL_YEAR_PATTERN.match(expression):
                year_ex = DateTimeUtil.GENERAL_YEAR_PATTERN.match(expression).group(1)
                comment = DateTimeUtil.get_year_ex(now, year_ex)
                date_time_comment_list.append(f"{expression}={comment}")
                continue




        return date_time_comment_list

    @staticmethod
    def get_year_ex(now: datetime, year_ex: str) -> str:
        year = now.year
        if year_ex == "今年":
            year = now.year
        elif year_ex == "去年":
            year = now.year - 1
        elif year_ex == "前年":
            year = now.year - 2
        elif year_ex == "明年":
            year = now.year + 1
        elif year_ex == "后年":
            year = now.year + 2
        return f"{year}年"

    @staticmethod
    def get_month_ex(now: datetime, month_ex: str) -> str:
        date_format = "%Y年%m月"
        if month_ex == "本月":
            return now.strftime(date_format)
        elif month_ex == "上月":
            last_month = now - timedelta(days=30)
            return last_month.strftime(date_format.replace("%Y", "%Y").replace("%m", "%m").replace("30", "01"))
        elif month_ex == "上上月":
            last_month = now - timedelta(days=60)
            return last_month.strftime(date_format.replace("%Y", "%Y").replace("%m", "%m").replace("30", "01"))
        elif month_ex == "下月":
            next_month = now + timedelta(days=30)
            return next_month.strftime(date_format.replace("%Y", "%Y").replace("%m", "%m").replace("30", "01"))
        elif month_ex == "去年本月":
            last_year = now.replace(year=now.year - 1)
            return last_year.strftime(date_format)
        return ""

    @staticmethod
    def get_day_ex(now: datetime, day_ex: str) -> str:
        date_format = "%Y年%m月%d日"
        comment = ""
        try:
            if day_ex == "今天":
                comment = now.strftime(date_format)
            elif day_ex == "昨天":
                comment = (now - timedelta(days=1)).strftime(date_format)
            elif day_ex == "前天":
                comment = (now - timedelta(days=2)).strftime(date_format)
            elif day_ex == "明天":
                comment = (now + timedelta(days=1)).strftime(date_format)
            elif day_ex == "后天":
                comment = (now + timedelta(days=2)).strftime(date_format)
            elif day_ex == "上月今天":
                previous_month = now + relativedelta(months=-1)
                comment = (previous_month.replace(day=now.day)).strftime(date_format)
            elif day_ex == "上上月今天":
                two_months_ago = now + relativedelta(months=-2)
                comment = (two_months_ago.replace(day=now.day)).strftime(date_format)

        except Exception as e:
            print(f"Error convert dayEx: {day_ex}, {e}")

        return comment

    @staticmethod
    def get_week_day_ex(now: datetime, x: int) -> str:
        # 计算本周第一天（周一）的日期
        monday = now - timedelta(days=now.weekday())
        # 通过加上(x - 1)天来得到本周第x天的日期
        desired_day = monday + timedelta(days=x - 1)
        return desired_day.strftime("%Y年%m月%d日")

    @staticmethod
    def get_general_week_day_ex(now: datetime, week_ex: str, day: int) -> str:
        this_monday = now - timedelta(days=now.weekday())
        desired_day = this_monday + timedelta(days=day - 1)

        if week_ex == "上周":
            desired_day -= timedelta(weeks=1)
        elif week_ex == "上上周":
            desired_day -= timedelta(weeks=2)
        elif week_ex == "下周":
            desired_day += timedelta(weeks=1)
        elif week_ex == "下下周":
            desired_day += timedelta(weeks=2)

        return desired_day.strftime("%Y年%m月%d日")

    @staticmethod
    def get_week_ex(now: datetime, week_ex: str) -> str:
        desire_monday = now - timedelta(days=now.weekday())
        desire_sunday = desire_monday + timedelta(days=6)

        if week_ex == "上周":
            desire_monday -= timedelta(weeks=1)
            desire_sunday -= timedelta(weeks=1)
        elif week_ex == "上上周":
            desire_monday -= timedelta(weeks=2)
            desire_sunday -= timedelta(weeks=2)
        elif week_ex == "下周":
            desire_monday += timedelta(weeks=1)
            desire_sunday += timedelta(weeks=1)
        elif week_ex == "下下周":
            desire_monday += timedelta(weeks=2)
            desire_sunday += timedelta(weeks=2)

        return f"{desire_monday.strftime('%Y年%m月%d日')}至{desire_sunday.strftime('%Y年%m月%d日')}"

    @staticmethod
    def get_specific_year_week_ex(now: datetime, year: int, week: int) -> str:
        first_day_of_year = datetime(year, 1, 1)
        target_week_first_day = first_day_of_year + timedelta(weeks=week - 1)
        target_week_last_day = target_week_first_day + timedelta(days=6)
        last_day_of_year = first_day_of_year.replace(month=12, day=31)

        if last_day_of_year < target_week_last_day:
            target_week_last_day = last_day_of_year

        return f"{target_week_first_day.strftime('%Y年%m月%d日')}至{target_week_last_day.strftime('%Y年%m月%d日')}"

    @staticmethod
    def get_general_year_week_ex(now: datetime, year_ex: str, week: int) -> str:
        year = now.year
        if year_ex == "去年":
            year -= 1
        elif year_ex == "前年":
            year -= 2
        elif year_ex == "明年":
            year += 1
        elif year_ex == "后年":
            year += 2
        return DateTimeUtil.get_specific_year_week_ex(now, year, week)

    @staticmethod
    def get_specific_year_month_week_ex(now: datetime, year: int, month: int, week: int) -> str:
        first_day_of_month = datetime(year, month, 1)
        target_week_first_day = first_day_of_month + timedelta(weeks=week - 1)
        target_week_last_day = target_week_first_day + timedelta(days=6)
        last_day_of_month = first_day_of_month + relativedelta(months=1, days=-1)

        if last_day_of_month < target_week_last_day:
            target_week_last_day = last_day_of_month

        return f"{target_week_first_day.strftime('%Y年%m月%d日')}至{target_week_last_day.strftime('%Y年%m月%d日')}"

    @staticmethod
    def get_general_year_month_week_ex(now: datetime, year_ex: str, month: int, week: int) -> str:
        year = now.year
        if year_ex == "去年":
            year -= 1
        elif year_ex == "前年":
            year -= 2
        elif year_ex == "明年":
            year += 1
        elif year_ex == "后年":
            year += 2
        return DateTimeUtil.get_specific_year_month_week_ex(now, year, month, week)

    @staticmethod
    def get_general_month_week_ex(now: datetime, month_ex: str, week: int) -> str:
        year = now.year
        month = now.month

        if month_ex == "上月":
            month -= 1
            if month <= 0:
                year -= 1
                month = 12
        elif month_ex == "上上月":
            month -= 2
            if month <= 0:
                year -= 1
                month += 12
        elif month_ex == "下月":
            month += 1
            if month > 12:
                year += 1
                month -= 12

        first_day_of_month = datetime(year, month, 1)
        target_week_first_day = first_day_of_month + timedelta(weeks=week - 1)
        target_week_last_day = target_week_first_day + timedelta(days=6)
        last_day_of_month = first_day_of_month + relativedelta(months=1, days=-1)

        if last_day_of_month < target_week_last_day:
            target_week_last_day = last_day_of_month

        return f"{target_week_first_day.strftime('%Y年%m月%d日')}至{target_week_last_day.strftime('%Y年%m月%d日')}"

    @staticmethod
    def get_specific_year_month_complete_week_ex(now: datetime, year: int, month: int, week: int) -> str:
        first_day_of_month = datetime(year, month, 1)
        first_monday = first_day_of_month + timedelta(days=(-first_day_of_month.weekday()) % 7)
        target_start_date = first_monday + timedelta(weeks=week - 1)
        target_end_date = target_start_date + timedelta(days=6)
        last_day_of_month = first_day_of_month + relativedelta(months=1, days=-1)

        if last_day_of_month < target_end_date:
            return ""  # Return empty string as per the original Java method behavior

        return f"{target_start_date.strftime('%Y年%m月%d日')}至{target_end_date.strftime('%Y年%m月%d日')}"

    @staticmethod
    def get_general_year_month_complete_week_ex(now: datetime, year_ex: str, month: int, week: int) -> str:
        year = now.year
        if year_ex == "去年":
            year -= 1
        elif year_ex == "前年":
            year -= 2
        elif year_ex == "明年":
            year += 1
        elif year_ex == "后年":
            year += 2
        return DateTimeUtil.get_specific_year_month_complete_week_ex(now, year, month, week)

    @staticmethod
    def get_general_month_complete_week_ex(now: datetime, month_ex: str, week: int) -> str:
        year = now.year
        month = now.month

        if month_ex == "上月":
            month -= 1
            if month <= 0:
                year -= 1
                month = 12
        elif month_ex == "上上月":
            month -= 2
            if month <= 0:
                year -= 1
                month += 12
        elif month_ex == "下月":
            month += 1
            if month > 12:
                year += 1
                month -= 12

        return DateTimeUtil.get_specific_year_month_complete_week_ex(now, year, month, week)

    @staticmethod
    def get_specific_year_complete_week_ex(now: datetime, year: int, week: int) -> str:
        first_day_of_year = datetime(year, 1, 1)
        first_monday = first_day_of_year + timedelta(days=(-first_day_of_year.weekday()) % 7)
        target_start_date = first_monday + timedelta(weeks=week - 1)
        target_end_date = target_start_date + timedelta(days=6)
        last_day_of_year = first_day_of_year + relativedelta(years=1, days=-1)

        if last_day_of_year < target_end_date:
            return ""

        return f"{target_start_date.strftime('%Y年%m月%d日')}至{target_end_date.strftime('%Y年%m月%d日')}"

    @staticmethod
    def get_general_year_complete_week_ex(now: datetime, year_ex: str, week: int) -> str:
        year = now.year
        if year_ex == "去年":
            year -= 1
        elif year_ex == "前年":
            year -= 2
        elif year_ex == "明年":
            year += 1
        elif year_ex == "后年":
            year += 2
        return DateTimeUtil.get_specific_year_complete_week_ex(now, year, week)

    @staticmethod
    def get_specific_year_month_last_week(now: datetime, year: int, month: int) -> str:
        last_day_of_month = calendar.monthrange(year, month)[1]
        last_date = datetime(year, month, last_day_of_month)
        last_day_of_month = datetime(year, month, last_day_of_month)
        while last_date.weekday() != 0:
            last_date -= timedelta(days=1)
        return f"{last_date.strftime('%Y年%m月%d日')}至{last_day_of_month.strftime('%Y年%m月%d日')}"

    @staticmethod
    def get_general_month_last_week(now: datetime, month_ex: str) -> str:
        year = now.year
        month = now.month

        if month_ex == "上月":
            month -= 1
            if month <= 0:
                year -= 1
                month = 12
        elif month_ex == "上上月":
            month -= 2
            if month <= 0:
                year -= 1
                month += 12
        elif month_ex == "下月":
            month += 1
            if month > 12:
                year += 1
                month -= 12

        return DateTimeUtil.get_specific_year_month_last_week(now, year, month)

    @staticmethod
    def get_specific_year_month_last_complete_week_ex(now: datetime, year: int, month: int) -> str:
        first_day_of_month = datetime(year, month, 1)
        last_sunday = first_day_of_month + relativedelta(months=1, days=-1)
        last_monday = last_sunday - timedelta(days=6)
        return f"{last_monday.strftime('%Y年%m月%d日')}至{last_sunday.strftime('%Y年%m月%d日')}"

    @staticmethod
    def get_general_month_last_complete_week_ex(now: datetime, month_ex: str) -> str:
        year = now.year
        month = now.month

        if month_ex == "上月":
            month -= 1
            if month <= 0:
                year -= 1
                month = 12
        elif month_ex == "上上月":
            month -= 2
            if month <= 0:
                year -= 1
                month += 12
        elif month_ex == "下月":
            month += 1
            if month > 12:
                year += 1
                month -= 12

        return DateTimeUtil.get_specific_year_month_last_complete_week_ex(now, year, month)

    @staticmethod
    def get_quarter_ex(now: datetime, quarter_ex: str) -> str:
        current_quarter = (now.month - 1) // 3 + 1
        last_quarter = 4 if current_quarter == 1 else current_quarter - 1
        next_quarter = 1 if current_quarter == 4 else current_quarter + 1
        current_year = now.year
        year_of_last_quarter = current_year if current_quarter != 1 else current_year - 1
        year_of_next_quarter = current_year + (1 if current_quarter == 4 else 0)
        year_of_same_quarter_last_year = current_year - 1
        comment = ""

        if quarter_ex == "本季度":
            comment = f"{current_year}年第{current_quarter}季度"
        elif quarter_ex == "上季度":
            comment = f"{year_of_last_quarter}年第{last_quarter}季度"
        elif quarter_ex == "下季度":
            comment = f"{year_of_next_quarter}年第{next_quarter}季度"
        elif quarter_ex == "去年本季度":
            comment = f"{year_of_same_quarter_last_year}年第{current_quarter}季度"

        return comment

    @staticmethod
    def get_recent_n_year(now: datetime, n: int) -> str:
        start_date = now - relativedelta(years=n)
        return f"{start_date.strftime('%Y年%m月%d日')}至{now.strftime('%Y年%m月%d日')}"

    @staticmethod
    def get_recent_n_month(now: datetime, n: int) -> str:
        start_date = now - relativedelta(months=n)
        return f"{start_date.strftime('%Y年%m月%d日')}至{now.strftime('%Y年%m月%d日')}"

    @staticmethod
    def get_recent_n_week(now: datetime, n: int) -> str:
        start_date = now - timedelta(weeks=n)
        return f"{start_date.strftime('%Y年%m月%d日')}至{now.strftime('%Y年%m月%d日')}"

    @staticmethod
    def get_recent_n_day(now: datetime, n: int) -> str:
        start_date = now - timedelta(days=n)
        return f"{start_date.strftime('%Y年%m月%d日')}至{now.strftime('%Y年%m月%d日')}"

    @staticmethod
    def get_recent_n_complete_year(now: datetime, n: int) -> str:
        if now.month == 12 and now.day == 31:
            end_date = now
        else:
            end_date = datetime(now.year, 12, 31) - relativedelta(years=1)
        start_date = end_date - relativedelta(years=n) + timedelta(days=1)
        return f"{start_date.strftime('%Y年%m月%d日')}至{end_date.strftime('%Y年%m月%d日')}"

    @staticmethod
    def get_recent_n_complete_month(now: datetime, n: int) -> str:
        current_month = now.month
        current_year = now.year
        if current_month > 2:
            start_month = current_month - 2
            start_year = current_year
        else:
            start_month = 12 + (current_month - 2)
            start_year = current_year - 1

        start_date = datetime(start_year, start_month, 1)

        end_month = current_month - 1
        end_year = current_year

        if end_month == 0:
            end_month = 12
            end_year -= 1

        end_date = datetime(end_year, end_month, calendar.monthrange(end_year, end_month)[1])

        return f"{start_date.strftime('%Y年%m月%d日')}至{end_date.strftime('%Y年%m月%d日')}"

    @staticmethod
    def get_recent_n_complete_quarter(now: datetime, n: int) -> str:
        if now.month % 3 == 0 and now.day == 31:
            end_date = now
        else:
            if now.month < 4:
                end_date = datetime(now.year - 1, 12, 31)
            elif now.month < 7:
                end_date = datetime(now.year, 3, 31)
            elif now.month < 10:
                end_date = datetime(now.year, 6, 30)
            else:
                end_date = datetime(now.year, 9, 30)

        start_date = end_date - relativedelta(months=n * 3) + timedelta(days=2)
        return f"{start_date.strftime('%Y年%m月%d日')}至{end_date.strftime('%Y年%m月%d日')}"

    @staticmethod
    def get_recent_n_complete_week(now: datetime, n: int) -> str:
        if now.weekday() == 6:  # Sunday
            end_date = now
        else:
            end_date = now - timedelta(weeks=1) + timedelta(days=(6 - now.weekday()))

        start_date = end_date - timedelta(weeks=n) + timedelta(days=1)
        return f"{start_date.strftime('%Y年%m月%d日')}至{end_date.strftime('%Y年%m月%d日')}"

    @staticmethod
    def get_recent_n_day_without_today(now: datetime, n: int) -> str:
        start_date = now - timedelta(days=n)
        end_date = now - timedelta(days=1)
        return f"{start_date.strftime('%Y年%m月%d日')}至{end_date.strftime('%Y年%m月%d日')}"

    @staticmethod
    def get_recent_n_quarter_with_current(now: datetime, n: int) -> str:
        if now.month < 4:
            end_date = datetime(now.year, 3, 31)
        elif now.month < 7:
            end_date = datetime(now.year, 6, 30)
        elif now.month < 10:
            end_date = datetime(now.year, 9, 30)
        else:
            end_date = datetime(now.year, 12, 31)

        start_date = end_date - relativedelta(months=n * 3 - 1)
        start_date = datetime(start_date.year, start_date.month, 1)
        return f"{start_date.strftime('%Y年%m月%d日')}至{end_date.strftime('%Y年%m月%d日')}"

    @staticmethod
    def get_month_last_day_ex(now: datetime, month_ex: str) -> str:
        month = now.month
        year = now.year
        if month_ex == "本月":
            next_month = month + 1 if month < 12 else 1
            next_year = year if month < 12 else year + 1
            first_of_next_month = datetime(year=next_year, month=next_month, day=1)
            last_day_of_this_month = first_of_next_month - relativedelta(days=1)
            comment = last_day_of_this_month.strftime('%Y年%m月%d日')
        elif month_ex == "上月":
            first_of_this_month = datetime(year=year, month=month, day=1)
            last_day_of_last_month = first_of_this_month - relativedelta(days=1)
            comment = last_day_of_last_month.strftime('%Y年%m月%d日')
        # if month_ex == "本月":
        #     comment = (now + relativedelta(day=1, months=1, days=-1)).strftime('%Y年%m月%d日')

        return comment

    @staticmethod
    def get_general_year_month_last_day_ex(now: datetime, year_ex: str, month: int) -> str:
        year = now.year
        if year_ex == "去年":
            year -= 1
        elif year_ex == "前年":
            year -= 2
        elif year_ex == "明年":
            year += 1
        elif year_ex == "后年":
            year += 2

        comment = (datetime(year, month, 1) + relativedelta(months=1, days=-1)).strftime('%Y年%m月%d日')
        return comment

    @staticmethod
    def get_specific_year_half_year_ex(now: datetime, year: int, half_year_ex: str) -> str:
        if half_year_ex == "上":
            start_date = datetime(year, 1, 1)
            end_date = datetime(year, 6, 30)
        else:
            start_date = datetime(year, 7, 1)
            end_date = datetime(year, 12, 31)

        return f"{start_date.strftime('%Y年%m月%d日')}至{end_date.strftime('%Y年%m月%d日')}"

    @staticmethod
    def get_general_year_half_year_ex(now: datetime, year_ex: str, half_year_ex: str) -> str:
        year = now.year
        if year_ex == "去年":
            year -= 1
        elif year_ex == "前年":
            year -= 2
        elif year_ex == "明年":
            year += 1
        elif year_ex == "后年":
            year += 2
        return DateTimeUtil.get_specific_year_half_year_ex(now, year, half_year_ex)

    @staticmethod
    def main():
        expressions = [
            "2024年02月29日",
            # "2023年02月29日",
            # "24年02月29日",
            # "今年2月29日",
            # "去年02月29日",
            "今年02月29日",
            "去年02月28日",
            "前年02月28日",
            "明年02月28日",
            "后年02月28日",
            # "本月31日",
            "本月30日",
            "上月31日",
            "上上月30日",
            "下月30日",
            "上月今天",
            "上上月今天",
            "今天",
            "昨天",
            "前天",
            "明天",
            "后天",
            "本周第1天",
            "本月最后一天",
            "上月最后一天",
            "今年02月最后一天",
            "2024年02月",
            "今年02月",
            "去年02月",
            "前年02月",
            "明年02月",
            "后年02月",
            "本月",
            "上月",
            "上上月",
            "下月",
            "去年本月",
            "2023年",
            "今年",
            "去年",
            "前年",
            "明年",
            "后年",
            "2024年第1季度",
            "今年第1季度",
            "去年第1季度",
            "前年第1季度",
            "明年第1季度",
            "后年第1季度",
            "本季度",
            "上季度",
            "下季度",
            "去年本季度",
            "2024年上半年",
            "2024年下半年",
            "今年上半年",
            "今年下半年",
            "去年上半年",
            "去年下半年",
            "上半年",
            "下半年",
            "本周星期3",
            "上周星期3",
            "上上周星期3",
            "下周星期3",
            "下下周星期3",
            "本周",
            "上周",
            "上上周",
            "下周",
            "下下周",
            "2024年第01周",
            "今年第01周",
            "今年第53周",
            "去年第01周",
            "前年第01周",
            "本月第2周",
            "上月第1周",
            "2024年02月最后一周",
            "2023年02月最后一周",
            "本月最后一周",
            "上月最后一周",
            "上上月最后一周",
            "2024年02月第4周",
            "今年02月第4周",
            "去年02月第4周",
            "前年02月第4周",
            "2024年02月第3个完整周",
            "今年02月第3个完整周",
            "去年02月第3个完整周",
            "前年02月第3个完整周",
            "2024年第01个完整周",
            "今年第01个完整周",
            "去年第01个完整周",
            "前年第01个完整周",
            "本月第1个完整周",
            "上月第1个完整周",
            "近2年",
            "近3个月",
            "近3周",
            "近3天",
            "近2个完整年",
            "近2个完整季度",
            "近2个完整月",
            "近2个完整周",
            "不包含今天的近3天",
            "包含当前季度的近2个季度"
        ]

        # print(DateTimeUtil.build_date_time_comment(expressions))

    @staticmethod
    def run(date_list):
        print(DateTimeUtil.build_date_time_comment(date_list))


if __name__ == "__main__":
    # DateTimeUtil.main()
    # DateTimeUtil.run()
    pass
