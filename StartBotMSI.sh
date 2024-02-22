#!/bin/bash
# cd /home/rusttm/PycharmProjects/SermanBot/MoiSklad/StartBotMSI.sh
# from https://stackoverflow.com/questions/43728431/relative-imports-modulenotfounderror-no-module-named-x
export PYTHONPATH="${PYTHONPATH}:/home/rusttm/PycharmProjects/SermanBot_v2/"
/home/rusttm/PycharmProjects/SermanBot_v2/pkg_env/bin/python /home/rusttm/PycharmProjects/SermanBot_v2/AiogramPackage/BOTMainPolling.py >> /home/rusttm/PycharmProjects/SermanBot_v2/bot.log 2>&1
