from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from handlers.pc_commands import open_file


class FileStates(StatesGroup):
    waiting_for_filename = State()


router = Router()


def get_main_inline_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🚀 start", callback_data="btn_start"),
                InlineKeyboardButton(text="❓ help", callback_data="btn_help")
            ],
            [
                InlineKeyboardButton(text="📂 open_file", callback_data="btn_open_file"),
                InlineKeyboardButton(text="👤 Мое имя", callback_data="btn_your_name")
            ],
            [
                InlineKeyboardButton(text="git of author", url="https://github.com/DChris19")
            ]
        ]
    )
    return keyboard


# commands

@router.message(Command("start"))
@router.message(F.text.lower() == "start")
async def cmd_start(message: Message):
    await message.answer("Hello honey\n\n /help", reply_markup=get_main_inline_keyboard())


@router.message(Command("help"))
@router.message(F.text.lower() == "help")
async def cmd_help(message: Message):
    await message.answer("commands list", reply_markup=get_main_inline_keyboard())


# callbacks

@router.callback_query(F.data == "btn_open_file")
async def ask_filename(callback: CallbackQuery, state: FSMContext):
    if callback.message:
        await callback.message.answer("Введи название файла:")
    await state.set_state(FileStates.waiting_for_filename)
    await callback.answer()


# FSM handlers

@router.message(FileStates.waiting_for_filename)
async def open_file_handler(message: Message, state: FSMContext):
    result = open_file(message.text or "")
    await message.answer(result)
    await state.clear()