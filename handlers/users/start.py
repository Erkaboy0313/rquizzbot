from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from keyboards.inline.keys import quiz,category_key,mode_key
from states.quizState import Quiz
from .nouns import nouns
from .verb import adjectives
from loader import dp
import asyncio
from random import randint,shuffle,choice
import logging
from data.config import ADMINS

@dp.message_handler(CommandStart(),state='*')
async def bot_start(message: types.Message):
    for admin in ADMINS:
        try:
            await message.bot.send_message(admin, f"Bot ishga tushirildi by {message.from_user.full_name}")

        except Exception as err:
            logging.exception(err)
    await message.answer(f"Salom👋 {message.from_user.full_name}! \nQaysi birini ustida ishlaymiz? 👇👇👇",reply_markup=category_key)
    await Quiz.category.set()


@dp.callback_query_handler(lambda call: call.data.startswith('ver'),state=Quiz.category)
async def category(call: types.CallbackQuery, state: FSMContext):
    cat = call.data.split('_')[1]
    await state.update_data({'category':cat})
    await call.message.delete()
    await call.message.answer(f"Perfect!!! Qaysi usulda ishlaymiz? 👇👇👇",reply_markup=mode_key)
    await Quiz.mode.set()
    
@dp.callback_query_handler(lambda call: call.data.startswith('mode'),state=Quiz.mode)
async def mode(call: types.CallbackQuery, state: FSMContext):
    mode = call.data.split('_')[1]
    await state.update_data({'mode':mode})
    await call.message.delete()
    if mode == "quiz":
        await Quiz.quiz.set()
        await start_quiz(state = state, call=call, new=True)
    elif mode == 'input':
        await Quiz.input.set()
        await start_input_mode(message=call.message,state=state,new=True)

#mistakes is not working    
@dp.callback_query_handler(lambda call: call.data.startswith('usr'),state=Quiz.quiz)
async def start_quiz(call: types.CallbackQuery,state: FSMContext, new: bool = False):
    data = await state.get_data()
    cat = data.get('category')
    quizs = data.get(cat,None)
    
    if cat == 'mistake' and not quizs:
        try:
            await asyncio.sleep(1)
            await call.message.delete()
        except:
            pass
        await Quiz.category.set()
        return await call.message.answer('Sizda xatolar mavjud emas!!!', reply_markup=category_key)
    
    elif not quizs:
        if cat == 'noun':
            quizs = list(nouns.keys())
        elif cat == 'adj':
            quizs = list(adjectives.keys())
    
    if not new:
        user_answer = call.data.split('_')[1]
        answer = data.get('asnwer')
        
        if not answer == user_answer:
            mistake_list = data.get('mistake',None)
            if not mistake_list:
                mistake_list = []
            mistake_list.append(answer)
            await state.update_data({'mistake':mistake_list})
            
        previous_words = data.get('prev_words')
        await call.message.edit_reply_markup(reply_markup=quiz(previous_words,answer))
        await asyncio.sleep(2)
        await call.message.delete()
        
        new_word = quizs.pop(randint(0,len(quizs)-1)) if len(quizs) > 1 else quizs.pop(0)
        await state.update_data({'asnwer':new_word})
        
        if cat == 'noun':
            a,b = choice(list(nouns.keys())),choice(list(nouns.keys()))
            words = [new_word,a,b]
            shuffle(words)
            await state.update_data({'prev_words':words})
            await call.message.answer(f"Toping? \n {nouns[new_word]} 🤔🤔🤔",reply_markup=quiz(words))    
        
        elif cat == 'adj':
            a,b = choice(list(adjectives.keys())),choice(list(adjectives.keys()))
            words = [new_word,a,b]
            shuffle(words)
            await state.update_data({'prev_words':words})
            await call.message.answer(f"Toping? \n {adjectives[new_word]} 🤔🤔🤔",reply_markup=quiz(words))    

        elif cat == 'mistake':
            a,b = choice(list(adjectives.keys())),choice(list(nouns.keys()))
            words = [new_word,a,b]
            shuffle(words)
            word = adjectives.get(new_word) if adjectives.get(new_word,None) else nouns.get(new_word)
            await state.update_data({'prev_words':words})
            await call.message.answer(f"Toping? \n {word} 🤔🤔🤔",reply_markup=quiz(words))
        
        await state.update_data({cat:quizs})
        
    else:
        new_word = quizs.pop(randint(0,len(quizs)-1)) if len(quizs) > 1 else quizs.pop(0)
        await state.update_data({'asnwer':new_word})
        
        if cat == 'noun':
            a,b = choice(list(nouns.keys())),choice(list(nouns.keys()))
            words = [new_word,a,b]
            shuffle(words)
            await state.update_data({'prev_words':words})
            await call.message.answer(f"Toping? \n {nouns[new_word]} 🤔🤔🤔",reply_markup=quiz(words))    
        elif cat == 'adj':
            a,b = choice(list(adjectives.keys())),choice(list(adjectives.keys()))
            words = [new_word,a,b]
            shuffle(words)
            await state.update_data({'prev_words':words})
            await call.message.answer(f"Toping? \n {adjectives[new_word]} 🤔🤔🤔",reply_markup=quiz(words))    
        
        elif cat == 'mistake':
            a,b = choice(list(adjectives.keys())),choice(list(nouns.keys()))
            words = [new_word,a,b]
            shuffle(words)
            word = adjectives.get(new_word) if adjectives.get(new_word,None) else nouns.get(new_word)
            await state.update_data({'prev_words':words})
            await call.message.answer(f"Toping? \n {word} 🤔🤔🤔",reply_markup=quiz(words))    
            
        await state.update_data({cat:quizs})

@dp.message_handler(state=Quiz.input)
async def start_input_mode(message: types.Message,state:FSMContext,new:bool = False):
    data = await state.get_data()
    cat = data.get('category')
    quizs = data.get(cat,None)
    
    if cat == 'mistake' and not quizs:
        try:
            await asyncio.sleep(1)
            await message.delete()
            previus_message = data.get('prev_message')
            await previus_message.delete()
        except:
            pass
        await Quiz.category.set()
        return await message.answer('Sizda xatolar mavjud emas!!!', reply_markup=category_key)
    
    elif not quizs :
        if cat == 'noun':
            quizs = list(nouns.keys())
        elif cat == 'adj':
            quizs = list(adjectives.keys())
                
    if not new:
        user_answer = message.text
        answer = data.get('asnwer')
        
        if not answer.lower() in user_answer.lower():
            sent = await message.answer(f"Sizning Javobingiz: {user_answer} ❌\n Javob: {answer}")
            mistake_list = data.get('mistake',None)
            if not mistake_list:
                mistake_list = []
            
            mistake_list.append(answer)
            await state.update_data({'mistake':mistake_list})
        else:
            sent = await message.answer(f"Sizning Javobingiz: {user_answer} ✅")
        previus_message = data.get('prev_message')
        await asyncio.sleep(2)
        await previus_message.delete()
        await message.delete()
        await sent.delete()
        
        new_word = quizs.pop(randint(0,len(quizs)-1)) if len(quizs) > 1 else quizs.pop(0)
        await state.update_data({'asnwer':new_word})
        
        if cat == 'noun':
            prev = await message.answer(f"So'zni tarjimasini yozing?🤔🤔🤔 \n{nouns[new_word]}")    
        elif cat == 'adj':
            prev = await message.answer(f"So'zni tarjimasini yozing?🤔🤔🤔 \n{adjectives[new_word]}")    
        elif cat == 'mistake':
            word = adjectives.get(new_word) if adjectives.get(new_word,None) else nouns.get(new_word)
            prev = await message.answer(f"So'zni tarjimasini yozing?🤔🤔🤔 \n{word}")
        await state.update_data({'prev_message':prev})
    
    else:
        new_word = quizs.pop(randint(0,len(quizs)-1)) if len(quizs) > 1 else quizs.pop(0)
        await state.update_data({'asnwer':new_word})
        if cat == 'noun':
            prev = await message.answer(f"So'zni tarjimasini yozing?🤔🤔🤔 \n{nouns[new_word]}")    
        elif cat == 'adj':
            prev = await message.answer(f"So'zni tarjimasini yozing?🤔🤔🤔 \n{adjectives[new_word]}")    
        elif cat == 'mistake':
            word = adjectives.get(new_word) if adjectives.get(new_word,None) else nouns.get(new_word)
            prev = await message.answer(f"So'zni tarjimasini yozing?🤔🤔🤔 \n{word}")
        await state.update_data({'prev_message':prev})
    
    await state.update_data({cat:quizs})
            
