from telebot import TeleBot, types
import asyncio
import yaml

with open("config.yaml") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)


bot = TeleBot(config["tg_bot_token"])


@bot.message_handler(commands=["help", "start"])
async def send_welcome(message):
    await bot.reply_to(
        message,
        "Hello",
    )


@bot.message_handler(commands=["admin"])
def any_msg(message):
    if message.from_user.id == int(config["tg_id"]):
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        check_delay = types.InlineKeyboardButton(
            text="Check delay", callback_data="check_delay"
        )
        send_delay = types.InlineKeyboardButton(
            text="Send delay", callback_data="send_delay"
        )
        channels = types.InlineKeyboardButton(text="Channels", callback_data="channels")
        keyboard.add(check_delay, send_delay, channels)
        bot.send_message(
            message.chat.id, "Choose what to change", reply_markup=keyboard
        )


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "check_delay":
        markup = types.ForceReply(selective=False)
        msg = bot.send_message(
            call.message.chat.id,
            f"Input new check delay. Now {config['time_to_sleep']}s",
            reply_markup=markup,
        )
        bot.register_next_step_handler(msg, change_check_delay)
    if call.data == "send_delay":
        markup = types.ForceReply(selective=False)
        msg = bot.send_message(
            call.message.chat.id,
            f"Input new check delay. Now {config['send_delay']}s",
            reply_markup=markup,
        )
        bot.register_next_step_handler(msg, change_send_delay)
    if call.data == "channels":
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        add = types.InlineKeyboardButton(text="Add", callback_data="add")
        delete = types.InlineKeyboardButton(text="Delete", callback_data="delete")
        keyboard.add(add, delete)
        bot.send_message(
            call.message.chat.id,
            f"Delete or add?\nNow  {config['vk_domain']}",
            reply_markup=keyboard,
        )
    if call.data == "delete":
        markup = types.ForceReply(selective=False)
        msg = bot.send_message(
            call.message.chat.id,
            "Input channel name you want to delete",
            reply_markup=markup,
        )
        bot.register_next_step_handler(msg, process_delete)
    if call.data == "add":
        markup = types.ForceReply(selective=False)
        msg = bot.send_message(
            call.message.chat.id,
            "Input channel name you want to add",
            reply_markup=markup,
        )
        bot.register_next_step_handler(msg, process_add)


ERROR_MSG = "Try again"


def change_check_delay(message):
    try:
        config["time_to_sleep"] = int(message.text)
        update_config(config)
    except:
        bot.send_message(message.chat.id, f"{ERROR_MSG}")


def change_send_delay(message):
    try:
        config["send_delay"] = int(message.text)
        update_config(config)
    except:
        bot.send_message(message.chat.id, f"{ERROR_MSG}")


def process_delete(message):
    try:
        config["vk_domain"].remove(message.text)
        update_config(config)
    except:
        bot.send_message(message.chat.id, f"{ERROR_MSG}")


def process_add(message):
    try:
        config["vk_domain"].append(message.text)
        update_config(config)
    except:
        bot.send_message(message.chat.id, f"{ERROR_MSG}")


def update_config(config):
    with open("config.yaml", "w") as f:
        config = yaml.dump(config, stream=f, default_flow_style=False, sort_keys=False)


def run():
    asyncio.run(bot.polling())


if __name__ == "__main__":
    run()
