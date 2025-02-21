from scapy.all import sniff, wrpcap, conf
import os

# Функція обробки перехоплених пакетів
def packet_callback(packet):
    # Визначення типу протоколу
    if packet.haslayer("TCP"):
        folder = "TCP"
    elif packet.haslayer("UDP"):
        folder = "UDP"
    elif packet.haslayer("ICMP"):
        folder = "ICMP"
    else:
        folder = "Other"
    
    # Перевірка наявності шифрування
    if packet.haslayer("TLS") or packet.haslayer("SSL"):
        encryption = "Encrypted"
    else:
        encryption = "Unencrypted"
    
    save_packet(packet, folder, encryption)

# Функція збереження пакетів у відповідний каталог
def save_packet(packet, folder, encryption):
    path = f"traffic/{folder}/{encryption}"
    os.makedirs(path, exist_ok=True)  # Створення директорії, якщо її немає
    filename = f"{path}/packets.pcap"
    
    # Збереження пакета в файл та додавання до існуючого
    wrpcap(filename, packet, append=True)
    
    # Виведення повідомлення в консоль
    print(f"Saved packet to {filename} - {folder} / {encryption}")

# Додана функція для перегляду збережених пакетів з сортуванням за іменем файлу
def list_saved_packets():
    packet_files = []
    for root, dirs, files in os.walk("traffic"):
        for file in files:
            if file.endswith(".pcap"):
                packet_files.append(os.path.join(root, file))
    
    # Сортування файлів
    packet_files.sort()
    
    for file in packet_files:
        print(file)

# Визначення мережевого інтерфейсу для перехоплення
default_iface = "enp2s0"  # Вказано інтерфейс enp2s0

print(f"Sniffing network traffic on interface: {default_iface}")

# Запуск прослуховування мережевого трафіку
sniff(iface=default_iface, prn=packet_callback, store=False)

