import paho.mqtt.client as mqtt
import time

Broker = "broker.hivemq.com"
Porta = 1883
Status = "automacao/refrigeracao"

def refrigeracao_control(client, userdata, message):

    comando = str(message.payload.decode("utf-8")).strip().lower()
    print(f'\n[Refrigeracao] Comando recebido: {comando}')

    if comando == "ligar arcondicionado":
        print("Arcondicionado ligado")

    elif comando == "desligar arcondicionado":
        print("arcondicionado desligado")

    else:
        print("Comando desconhecido")

     
     
     
cliente = mqtt.Client()
cliente.on_message = refrigeracao_control

print("conectando ao broker...")

try:
    cliente.connect(Broker, Porta)
    cliente.subscribe(Status)
    cliente.loop_start()
    print("cliente conectado com sucesso")
except Exception as e:
    print(f"Erro ao conectar ao Broker: {e}")
else:
    try:
        while True:
            print("\n---Menu de Automacao de refrigeracao---")
            print("1. Ligar arcondicionado")
            print("2. Desligar arcondicionado")
            print("3. Sair")

            try:
                opcao = int(input("Escolha uma opcao: "))
            except ValueError:
                print("Entrada invalida, informe um numero.")
                continue

            if opcao == 1:
                cliente.publish(Status, "ligar arcondicionado")
                time.sleep(0.5)

            elif opcao == 2:
                cliente.publish(Status, "desligar arcondicionado")
                time.sleep(0.5)

            elif opcao == 3:
                break

            else:
                print("Opcao invalida")

            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nSaindo...")
    finally:
        cliente.loop_stop()
        cliente.disconnect()