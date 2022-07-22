import tkinter
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

HOST = "localhost"
PORT = 55000
if not PORT:
    PORT = 55000
else:
    PORT = int(PORT)

BUFF_SIZE = 1024
ADDRESS = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDRESS)


def receive_message():
    while True:
        try:
            msg = client_socket.recv(BUFF_SIZE).decode("utf8")
            split_msg = msg.split("@")
            print(split_msg)

            if len(split_msg) == 1:
                list_msg.insert(tkinter.END, msg)
                print(msg)

            if len(split_msg) > 1:
                receiver = split_msg[1]
                print(receiver)
                if receiver == client_name.get():
                    print(split_msg)
                    list_msg.insert(tkinter.END, "De: " + split_msg[0])
                    list_msg.insert(tkinter.END, "Assunto: " + split_msg[2])
                    list_msg.insert(tkinter.END, "Mensagem: " + split_msg[3])

        except OSError:
            break


def submit_name():
    name = client_name.get()
    print(name)
    client_socket.send(bytes(name, "utf8"))


def submit():
    if (client_msg != "") and (client_receiver != ""):
        msg = "@" + client_receiver.get() + "@" + client_subject.get() + "@" + client_msg.get()

        # clear the input
        client_receiver.set("")
        client_subject.set("")
        client_msg.set("")

        client_socket.send(bytes(msg, "utf8"))


def disconnect():
    msg = "{disconnect}"
    client_socket.send(bytes(msg, "utf8"))
    client_socket.close()
    window.quit()


def close_page():
    client_msg.set("{disconnect}")
    submit()


window = tkinter.Tk()
window.title("Client")
window.configure(bg="#2a76c7")


client_name = tkinter.StringVar()
client_receiver = tkinter.StringVar()
client_subject = tkinter.StringVar()
client_msg = tkinter.StringVar()



label_name = tkinter.Label(window, text="Digite seu nickname:", height=2, bg="#2a76c7", font="Verdana 11 bold")
label_receiver = tkinter.Label(window, text="Destinatário:", width=10, height=2, bg="#2a76c7", font="Verdana 11 bold")
label_msg = tkinter.Label(window, text="Mensagem:", width=10, height=2, bg="#2a76c7", font="Verdana 11 bold")



frame_msg = tkinter.Frame(window)
bar = tkinter.Scrollbar(frame_msg)
list_msg = tkinter.Listbox(window, yscrollcommand=bar.set, width=40, height=10, border=2, font="Verdana 11 bold")



input_name = tkinter.Entry(window, textvariable=client_name, font="Verdana 11 bold")
input_name.bind("<Return>", )
input_receiver = tkinter.Entry(window, textvariable=client_receiver, font="Verdana 11 bold")
input_receiver.bind("<Return>", )
input_subject = tkinter.Entry(window, textvariable=client_subject, font="Verdana 11 bold")
input_subject.bind("<Return>", )
input_msg = tkinter.Entry(window, textvariable=client_msg, font="Verdana 11 bold")
input_msg.bind("<Return>", )

window.protocol("WM_DELETE_WINDOW", close_page)


b_submit_name = tkinter.Button(window, command=submit_name, text="Enviar nome", border=2, font="Verdana 11 bold",
                               bg="#2a76c7")
b_submit = tkinter.Button(window, command=submit, text="Enviar Email", border=2, font="Verdana 11 bold",
                          bg="#2a76c7")
b_disconnect = tkinter.Button(window, command=disconnect, text="Desconectar", border=2, font="Verdana 11 bold",
                              bg="#2a76c7")



label_name.grid(row=1, column=1, sticky="w")
label_receiver.grid(row=3, column=1, sticky="w")
label_msg.grid(row=5, column=1, sticky="w")


bar.grid()
list_msg.grid(row=10, column=1, columnspan=2)
frame_msg.grid()

input_name.grid(row=1, column=2)
input_receiver.grid(row=3, column=2)
input_msg.grid(row=5, column=2)

b_submit_name.grid(row=2, column=2, sticky="n")
b_submit.grid(row=6, column=2, sticky="n")
b_disconnect.grid(row=11, column=1, columnspan=3)


receive_thread = Thread(target=receive_message)
receive_thread.start()


window.mainloop()





