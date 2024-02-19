import heapq
from collections import Counter, defaultdict
from math import *
# Функция для проведения статического анализа текста и записи результатов в файл
def analyze_text(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        text = file.read()
    # Считаем частоту символов
    char_freq = Counter(text)
    total_chars = sum(char_freq.values())
    # Считаем частоту пар символов
    pair_freq = Counter(zip(text, text[1:]))
    # Записываем результаты в файл Analyze.txt
    with open('Analyze.txt', 'w', encoding='utf-8') as analyze_file:
        analyze_file.write("Character frequencies:\n")
        for char, freq in char_freq.items():
            analyze_file.write(f"{char}: {freq:}\n")
        analyze_file.write("\nPair frequencies:\n")
        for pair, freq in pair_freq.items():
            analyze_file.write(f"{''.join(pair)}: {freq:}\n")
    return char_freq, pair_freq

# Функция для построения кода Хаффмана и записи его в файл
def build_huffman_code(char_freq):
    heap = [[weight, [char, ""]] for char, weight in char_freq.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])

    huffman_code = dict(sorted(heapq.heappop(heap)[1:], key=lambda p: (len(p[-1]), p)))

    # Записываем код Хаффмана в файл Code.txt
    with open('Code.txt', 'w', encoding='utf-8') as code_file:
        for char, code in huffman_code.items():
            code_file.write(f"{char}: {code}\n")
    return huffman_code

# Функция для кодирования текста с использованием кода Хаффмана
def encode_text_with_huffman(text, huffman_code):
    encoded_text = ''.join(huffman_code[char] for char in text)
    return encoded_text

# Функция для декодирования текста с использованием кода Хаффмана
def decode_text_with_huffman(encoded_text, huffman_code):
    reversed_huffman_code = {code: char for char, code in huffman_code.items()}
    decoded_text = ''
    code = ''
    for bit in encoded_text:
        code += bit
        if code in reversed_huffman_code:
            decoded_text += reversed_huffman_code[code]
            code = ''
    return decoded_text

# Анализируем текст и записываем результаты в файл
char_freq, pair_freq = analyze_text('lab4.txt')

# Строим код Хаффмана и записываем его в файл
huffman_code = build_huffman_code(char_freq)

# Кодируем текст с использованием кода Хаффмана и записываем результат в файл
with open('lab4.txt', 'r', encoding='utf-8') as file:
    text = file.read()

encoded_text = encode_text_with_huffman(text, huffman_code)

with open('Text_Huffman.txt', 'w', encoding='utf-8') as encoded_file:
    encoded_file.write(encoded_text)

# Декодируем текст и записываем результат в файл
decoded_text = decode_text_with_huffman(encoded_text, huffman_code)

with open('Decoded_Text.txt', 'w', encoding='utf-8') as decoded_file:
    decoded_file.write(decoded_text)

#функция, которая создает равномерный 5-битовый код
def build_uniform_5_bit_code(char_freq):
    code = {}
    current_code = '00000'
    for char in sorted(char_freq.keys()):
        code[char] = current_code
        current_code = bin(int(current_code, 2) + 1)[2:].zfill(5)
    return code

# Строим равномерный 5-битовый код
uniform_5_bit_code = build_uniform_5_bit_code(char_freq)

# Записываем равномерный 5-битовый код в файл Code_5.txt
with open('Code_5.txt', 'w', encoding='utf-8') as code_file_5_bit:
    for char, code in uniform_5_bit_code.items():
        code_file_5_bit.write(f"{char}: {code}\n")

# Кодируем текст с использованием равномерного 5-битового кода и записываем результат в файл
encoded_text_5_bit = ''.join(uniform_5_bit_code[char] for char in text)

with open('Text_5_code.txt', 'w', encoding='utf-8') as encoded_file_5_bit:
    encoded_file_5_bit.write(encoded_text_5_bit)

# Подсчитываем количество бит в файлах Text_Huffman.txt и Text_5_code.txt и выводим результат в консоль
bit_count_huffman = len(encoded_text)
bit_count_5_bit = len(encoded_text_5_bit)

# Функция для вычисления количества информации по формуле Шеннона
def shannon_entropy(char_freq):
    entropy = 0
    total_chars = sum(char_freq.values())
    for freq in char_freq.values():
        probability = freq / total_chars
        entropy -= probability * log2(probability)
    return entropy

# Сравниваем с количеством информации по формуле Шеннона
shannon_bits = shannon_entropy(char_freq) * 15487
print(f"Количество бит по формуле Шеннона: {shannon_bits}")
def lzw_encode(text):
    dictionary = {chr(i): i for i in range(256)}
    result = []
    current_code = 256
    w = ""
    for char in text:
        wc = w + char
        if wc in dictionary:
            w = wc
        else:
            result.append(dictionary[w])
            dictionary[wc] = current_code
            current_code += 1
            w = char
    if w:
        result.append(dictionary[w])
    return result

# Чтение текста из файла
with open('lab4.txt', 'r', encoding='utf-8') as file:
    text = file.read()

# Кодирование текста LZW
encoded_text_lzw = lzw_encode(text)

# Запись закодированного текста в файл Text_LZW.txt
with open('Text_LZW.txt', 'w', encoding='utf-8') as encoded_file_lzw:
    encoded_file_lzw.write(' '.join(map(str, encoded_text_lzw)))

# Вычисление количества бит закодированного текста
num_bits_lzw = len(''.join(bin(code)[2:].zfill(9) for code in encoded_text_lzw))

# Вывод количества бит в консоль
print(f"Количество бит закодированного текста LZW: {num_bits_lzw}")
print(f"Количество бит в файле Text_Huffman.txt: {bit_count_huffman}")
print(f"Количество бит в файле Text_5_code.txt: {bit_count_5_bit}")
