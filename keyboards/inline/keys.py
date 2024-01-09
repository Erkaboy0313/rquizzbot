from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup

def quiz(words,answer = None):
    quiz = InlineKeyboardMarkup(row_width=1)
    if answer:
        for word in words:
            if answer == word:
                quiz.insert(InlineKeyboardButton(text=f"{word} ✅", callback_data=f'usr_{word}'))
            else:
                quiz.insert(InlineKeyboardButton(text=f"{word} ❌", callback_data=f'usr_{word}'))
    else:
        for word in words:
            quiz.insert(InlineKeyboardButton(text=f"{word}", callback_data=f'usr_{word}'))
    return quiz


category_key = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Noun', callback_data="ver_noun"),
         InlineKeyboardButton(text='Adjective', callback_data='ver_adj')],
        [InlineKeyboardButton(text='Mistakes', callback_data='ver_mistake')]   
    ]
)

mode_key = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Quiz mode', callback_data="mode_quiz")],
        [InlineKeyboardButton(text='Input mode', callback_data='mode_input')]   
    ]
)
  