import asyncio

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, BufferedInputFile
from handlers.pc_commands import open_file, shutdown, rebooting, take_screenshot


class FileStates(StatesGroup):
    waiting_for_filename = State()


router = Router()


def get_main_inline_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🖱️start", callback_data="btn_start"),
                InlineKeyboardButton(text="📞help", callback_data="btn_help")
            ],
            [
                InlineKeyboardButton(text="📁open file", callback_data="btn_open_file"),
            ],
            [
                InlineKeyboardButton(text="🛑shutdown", callback_data="btn_shutdown"),
                InlineKeyboardButton(text="⚙️reboot", callback_data="btn_rebooting")
            ],
            [
                InlineKeyboardButton(text="📷screenshot", callback_data="btn_screenshot"),
            ],
            [
                InlineKeyboardButton(text="💻git of author", url="https://github.com/DChris19")
            ]
        ]
    )
    return keyboard


# commands
@router.message(Command("start"))
@router.message(F.text.lower() == "start")
async def cmd_start(message: Message):
    name = message.from_user.first_name if message.from_user else "honey"
    await message.answer(f"Hello honey {name}♥️", reply_markup=get_main_inline_keyboard())


@router.message(Command("help"))
@router.message(F.text.lower() == "help")
async def cmd_help(message: Message):
    await message.answer("commands list", reply_markup=get_main_inline_keyboard())


# callbacks
@router.callback_query(F.data == "btn_start")
async def cb_start(callback: CallbackQuery):
    if callback.message:
        name = callback.from_user.first_name if callback.from_user else "honey"
        await callback.message.answer(f"Hello honey {name}♥️", reply_markup=get_main_inline_keyboard())
    await callback.answer()


@router.callback_query(F.data == "btn_help")
async def cb_help(callback: CallbackQuery):
    if callback.message:
        await callback.message.answer("commands list", reply_markup=get_main_inline_keyboard())
    await callback.answer()


@router.callback_query(F.data == "btn_open_file")
async def ask_filename(callback: CallbackQuery, state: FSMContext):
    if callback.message:
        await callback.message.answer("Enter file name:")
    await state.set_state(FileStates.waiting_for_filename)
    await callback.answer()


@router.callback_query(F.data == "btn_shutdown")
async def cb_shutdown(callback: CallbackQuery):
    if callback.message:
        await callback.message.answer(shutdown())
    await callback.answer()


@router.callback_query(F.data == "btn_rebooting")
async def cb_rebooting(callback: CallbackQuery):
    if callback.message:
        await callback.message.answer(rebooting())
    await callback.answer()


@router.callback_query(F.data == "btn_screenshot")
async def cb_screenshot(callback: CallbackQuery):
    if callback.message:
        await callback.message.answer("Taking screenshot...")
    await callback.answer()

    screenshot_bytes = await asyncio.to_thread(take_screenshot)

    if callback.message:
        if screenshot_bytes is None:
            await callback.message.answer(
                "Failed to take screenshot. Make sure Pillow is installed (pip install Pillow)."
            )
        else:
            photo = BufferedInputFile(screenshot_bytes, filename="screenshot.png")
            await callback.message.answer_photo(photo)


# FSM handlers
@router.message(FileStates.waiting_for_filename)
async def open_file_handler(message: Message, state: FSMContext):
    result = open_file(message.text or "")
    await message.answer(result)
    await state.clear()