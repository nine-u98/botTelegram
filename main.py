import telebot
import os
import pytube

bot = telebot.TeleBot('5866057229:AAEVrCc2Zp7MgfL-jHGoM1HxNtuWvBLxcO0')

#directorio donde guardar la descarga
path = os.getcwd() + "/slide/"

def main():
        bot.polling()

@bot.message_handler(commands=['descargar'])
def musica(message):
    texto = message.text
    chat = message.chat.id
    l = len(texto)
    url = texto[8:l]
    #URL del video de Youtube
    try:
        yt = pytube.YouTube(url)
        bot.reply_to(message, 'El video - '+yt.title+' - se esta descargando.')

        #Filtramos las descargas por audio solamente, orden descendiente de calidad y
        # el primero que será el que tiene la calidad más alta
        stream = yt.streams.get_highest_resolution()
        #nombre = stream.default_filename
        #quitamos espacios y paréntesis y cambiamos el tipo de fichero a mp3
        nombre = stream.default_filename
        nombre = ''.join(char for char in nombre if char.isalnum())
        nombre = nombre.replace(" ", "")
        nombre = nombre.replace("(", "-")
        nombre = nombre.replace(")", "-")
        nombre = nombre.replace("mp4", ".mp4")
        #Descargamos el audio seleccionado en el directorio escogido
        stream.download(output_path=path,filename=nombre)
        #enviar imagen del audio (portada, es el thumbnail del video);
        #enviar audio:
        bot.send_document(chat_id=chat, document=open(path+nombre, 'rb'))

        #borrar archivo de musica (solo pasa si se envia sin error)
        operation = 'rm '+path+nombre
        os.system(operation)
    except pytube.exceptions.RegexMatchError:
        bot.send_message(chat,'URL de vídeo no existe')
        print("URL no encontrada")
    except BaseException as err:
        print(f"Unexpected {err=}, {type(err)=}")
        bot.send_message(chat, 'Se ha producido un error')

if __name__ == '__main__':
    main()