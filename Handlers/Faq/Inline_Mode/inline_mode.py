from aiogram import types
from aiogram.types import InputTextMessageContent, InlineQueryResultArticle

from Handlers.Faq.Inline_Mode.query_analizing import QueryAnalizer


async def process_query(query: types.InlineQuery):
    if query.query == '':
        await query.answer(
            results=[
                types.InlineQueryResultArticle(
                    id='none',
                    title='Напишите что хотите узнать',
                    input_message_content=types.InputTextMessageContent(
                        message_text='Введите запрос после @BOTTEC_Testbot'
                    )
                )
            ],
            cache_time=1
        )
    else:
        results_here = process_words(query)
        await query.answer(
            results=results_here,
            cache_time=1
        )


def process_words(query):
    q_a = QueryAnalizer()
    query_here = query.query.lower()
    results_here = []
    words = q_a.process_query(text=query_here)
    answers = q_a.get_answers(words)
    for i, w in enumerate(words):
        results_here.append(
            InlineQueryResultArticle(
                id=i+1,
                title=f'{w}',
                input_message_content=InputTextMessageContent(
                    message_text=f'{answers[i]}',
                ),
            )
        )
    return results_here

