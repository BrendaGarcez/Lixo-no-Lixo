import os
import random

def load_images_from_folder(folder_path):
    """
    Carrega todas as imagens de uma pasta e retorna uma lista com os caminhos dos arquivos.
    
    Parâmetros:
        - folder_path (str): Caminho da pasta.
    
    Retorno:
        - Lista de caminhos dos arquivos de imagem.
    """
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"A pasta '{folder_path}' não existe.")
    
    images = []
    for file_name in os.listdir(folder_path):
        if file_name.lower().endswith((".png", ".jpg", ".jpeg")):  # Filtrar formatos de imagem
            images.append(os.path.join(folder_path, file_name))
    return images

def generate_image_sequence(phase_folder, max_images):
    """
    Gera uma sequência de imagens intercaladas aleatoriamente entre corretas e erradas, sem repetir.
    
    Parâmetros:
        - phase_folder (str): Caminho da pasta da fase (ex.: "jogo_imagens/fase1").
        - max_images (int): Quantidade máxima de imagens na sequência.
    
    Retorno:
        - Uma lista de caminhos das imagens intercaladas.
    """
    correct_folder = os.path.join(phase_folder, "corretas")
    wrong_folder = os.path.join(phase_folder, "erradas")
    
    # Carregar imagens de ambas as pastas
    correct_images = load_images_from_folder(correct_folder)
    wrong_images = load_images_from_folder(wrong_folder)
    
    if not correct_images and not wrong_images:
        raise ValueError("Nenhuma imagem encontrada nas pastas 'corretas' ou 'erradas'.")
    
    # Embaralhar listas
    random.shuffle(correct_images)
    random.shuffle(wrong_images)
    
    # Criar sequência intercalada
    sequence = []
    while len(sequence) < max_images and (correct_images or wrong_images):
        if correct_images:
            sequence.append(correct_images.pop(0))  # Adicionar imagem correta
        if wrong_images and len(sequence) < max_images:
            sequence.append(wrong_images.pop(0))  # Adicionar imagem errada
    
    return sequence
