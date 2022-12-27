from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters


def start(update: Update, context: CallbackContext) -> None:
    str = ''


def reply(update: Update, context: CallbackContext) -> None:
    query = update.message.text.lower()

    def deleter(folder):
        import os, shutil
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

    path = 'text.txt'
    text = open(path, 'r', encoding='utf-8')
    readed = text.read()
    print(text.tell())
    # print(readed)

    from textrazor import TextRazor

    client = TextRazor(
        'cc2a8555b9c4109fb6e8bcec2cdb2c128ad29f1b7b87dcc67e6eb2fa',
        extractors=["entities"])

    response = client.analyze(query)

    ent = response.entities()
    if not ent:
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text='Sorry, but your text is to short for me to analyse')
        return
    print(ent)
    topic = str(ent[0].id)
    print(topic)

    import os
    from bing_image_downloader import downloader
    isdir = os.path.isdir('dataset')
    if (isdir):
        deleter('dataset')
    downloader.download(topic,
                        limit=4,
                        output_dir='dataset',
                        adult_filter_off=True,
                        force_replace=False,
                        timeout=60,
                        verbose=True)

    def run_fast_scandir(dir, ext):  # dir: str, ext: list
        subfolders, files = [], []

        for f in os.scandir(dir):
            if f.is_dir():
                subfolders.append(f.path)
            if f.is_file():
                if os.path.splitext(f.name)[1].lower() in ext:
                    files.append(f.path)

        for dir in list(subfolders):
            sf, f = run_fast_scandir(dir, ext)
            subfolders.extend(sf)
            files.extend(f)
        return subfolders, files

    folder = 'dataset'
    subfolders, files = run_fast_scandir(folder, [".jpg", ".png"])
    for i in files:
        phot = open(i, 'rb')
        context.bot.send_photo(chat_id=update.message.chat_id, photo=phot)


def main():
    API_KEY = '5941016762:AAGmGLXtD4vQlnzfC5ijsrozYCcElVRyDuA'
    updater = Updater(API_KEY, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.text, reply))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
