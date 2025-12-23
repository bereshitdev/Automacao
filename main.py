import network
import urequests
import ujson
import time
from machine import Pin, I2C
import ssd1306

# 1. Configuração do Ecrã OLED
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# 2. Função para ligar ao Wi-Fi do Wokwi
def liga_wifi():
    print("A ligar ao Wi-Fi", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect('Wokwi-GUEST', '')
    while not sta_if.isconnected():
        print(".", end="")
        time.sleep(0.1)
    print(" Conectado!")

# 3. Função para desenhar a seta de variação
def desenha_seta(x, y, subiu):
    if subiu:
        # Seta para cima
        oled.line(x, y, x+4, y-4, 1)
        oled.line(x+4, y-4, x+8, y, 1)
        oled.line(x+4, y-4, x+4, y+4, 1)
    else:
        # Seta para baixo
        oled.line(x, y, x+4, y+4, 1)
        oled.line(x+4, y+4, x+8, y, 1)
        oled.line(x+4, y+4, x+4, y-4, 1)

# --- Execução Principal ---
liga_wifi()

url_api = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_24hr_change=true"

while True:
    try:
        oled.fill(0)
        oled.text("A atualizar...", 0, 0)
        oled.show()

        # Faz a requisição à API
        resposta = urequests.get(url_api)
        dados = ujson.loads(resposta.text)
        
        preco = dados['bitcoin']['usd']
        variacao = dados['bitcoin']['usd_24h_change']
        
        # Limpa e desenha o Dashboard
        oled.fill(0)
        oled.text("BITCOIN (BTC)", 10, 0)
        oled.framebuf.line(0, 12, 127, 12, 1)
   
   
        oled.text(f"USD: {preco:,}", 0, 25)
        
        # Lógica da variação
        txt_var = f"{variacao:.2f}%"
        oled.text(txt_var, 0, 45)
        desenha_seta(60, 48, variacao > 0)
        
        oled.show()
        resposta.close()

    except Exception as e:
        print("Erro ao procurar dados:", e)
        oled.fill(0)
        oled.text("Erro API", 0, 0)
        oled.show()

    time.sleep(30) # Atualiza a cada 30 segundos